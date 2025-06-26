# books/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.generics import get_object_or_404

from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer
from .utils import get_author_data, call_openai, generate_tts_audio, get_ai_summary_fallback
from .recommender import recommend_by_description_similarity, recommend_by_threads_similarity


# 카테고리 전체 목록 조회
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# 도서 전체 목록 조회 및 도서 등록 (GET, POST)
@api_view(['GET', 'POST'])
def book_list_create(request):
    if request.method == 'GET':
        # 검색, 필터, 정렬 조건 처리
        query = request.GET.get('q')
        category_id = request.GET.get('category')
        ordering = request.GET.get('ordering', 'id')

        books = Book.objects.all()
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(description__icontains=query)
            )
        if category_id:
            books = books.filter(category_id=category_id)
        books = books.order_by(ordering)

        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        # 중복 책 등록 방지 및 유효성 검사
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get("title")
            author = serializer.validated_data.get("author")
            publisher = serializer.validated_data.get("publisher")

            if Book.objects.filter(title=title, author=author, publisher=publisher).exists():
                return Response(
                    {"error": "이미 동일한 제목, 저자, 출판사의 책이 등록되어 있습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            book = serializer.save()
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 도서 상세 정보 조회, 수정, 삭제 (GET, PUT, DELETE)
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_update_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'GET':
        # 작가 정보가 없을 경우 AI를 통해 보완
        if not book.author_info or not book.author_works:
            try:
                print(f"[AI 처리] {book.title} / {book.author}")
                summary, _, major_works = get_author_data(book.author)
                if not summary:
                    gpt_result = get_ai_summary_fallback(book.author)
                    book.author_info = gpt_result.get("author_info")
                    book.author_works = gpt_result.get("author_works")
                else:
                    gpt_result = call_openai(book.title, book.author, summary, major_works)
                    book.author_info = gpt_result.get("author_info")
                    book.author_works = gpt_result.get("author_works")
                book.save()
            except Exception as e:
                print(f"[GPT 처리 실패] {book.title}: {e}")

        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 위키 기반 작가 대표작 추출 API
@api_view(['GET'])
def author_works_from_wiki(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    works = get_author_data(book.author)[2]
    return Response({"author": book.author, "works": works})


# TTS 오디오 파일 재생성 요청 API
@api_view(['POST'])
def regenerate_tts_audio(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    text = f"{book.title} / {book.author_info} / {book.author_works}"
    audio_path = generate_tts_audio(book.pk, text)

    if audio_path:
        book.tts_audio.name = audio_path
        book.save()
        return Response({
            "message": "TTS 오디오 생성 성공",
            "tts_audio": book.tts_audio.url
        }, status=200)

    return Response({"error": "TTS 생성 실패"}, status=500)


# 도서 좋아요 토글 기능 (로그인 필요)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_book_like(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    if book.liked_users.filter(pk=user.pk).exists():
        book.liked_users.remove(user)
        liked = False
    else:
        book.liked_users.add(user)
        liked = True

    return Response({
        "liked": liked,
        "likes_count": book.liked_users.count(),
    })


# 개인화 추천 (좋아요 기반 또는 감상글 기반)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def personal_recommendation(request):
    user = request.user
    rec_type = request.GET.get('type', 'likes')  # 기본값은 'likes'

    if rec_type == 'threads':
        recommended_books = recommend_by_threads_similarity(user)
    elif rec_type == 'likes':
        recommended_books = recommend_by_description_similarity(user)

    serializer = BookSerializer(recommended_books, many=True, context={'request': request})
    return Response(serializer.data)


# MBTI 기반 도서 추천
@api_view(['GET'])
def mbti_book_recommendation(request):
    mbti = request.GET.get('mbti', '').upper()

    # MBTI 유형에 따른 추천 카테고리 및 설명
    mbti_map = {
    "INTJ": {
        "categories": [4, 5],  # 인문·사회, 과학·IT
        "reason": "이론적 사고와 구조적 분석을 선호하며, 깊이 있는 탐구를 즐깁니다."
    },
    "INTP": {
        "categories": [1, 5],  # 문학·에세이·만화, 과학·IT
        "reason": "탐구심이 강하고 추상적 개념과 지식을 혼자만의 관점으로 해석하기 좋아합니다."
    },
    "ENTJ": {
        "categories": [2, 4],  # 경제·경영, 인문·사회
        "reason": "리더십과 전략 수립에 능하며, 사회구조나 정책에도 관심이 많습니다."
    },
    "ENTP": {
        "categories": [3, 5],  # 자기계발, 과학·IT
        "reason": "새로운 아이디어와 혁신을 추구하며, 도전적이고 다재다능한 성향을 보입니다."
    },
    "INFJ": {
        "categories": [1, 6],  # 문학·에세이·만화, 어린이·청소년
        "reason": "이상주의적이면서도 타인의 감정에 민감하며, 깊은 내면의 세계를 가지고 있습니다."
    },
    "INFP": {
        "categories": [1, 7],  # 문학·에세이·만화, 취미·실용·여행
        "reason": "자기 성찰과 창작 활동을 선호하고, 감성적으로 풍부한 콘텐츠에 끌립니다."
    },
    "ENFJ": {
        "categories": [3, 6],  # 자기계발, 어린이·청소년
        "reason": "타인을 돕고 영감을 주는 데 관심이 많으며, 교육적 가치도 중시합니다."
    },
    "ENFP": {
        "categories": [3, 7],  # 자기계발, 취미·실용·여행
        "reason": "활기차고 호기심이 많으며, 다양한 경험과 자아 발견을 즐깁니다."
    },
    "ISTJ": {
        "categories": [2, 8],  # 경제·경영, 학습·참고서
        "reason": "논리적이고 체계적인 정보 습득을 선호하며, 실용성과 정확성을 중시합니다."
    },
    "ISFJ": {
        "categories": [6, 8],  # 어린이·청소년, 학습·참고서
        "reason": "헌신적이고 보호자 같은 성향으로, 교육과 실천적 지식에 관심이 많습니다."
    },
    "ESTJ": {
        "categories": [2, 3],  # 경제·경영, 자기계발
        "reason": "실용적이고 목표지향적인 성향으로, 조직 관리와 자기 효율화에 관심이 많습니다."
    },
    "ESFJ": {
        "categories": [6, 7],  # 어린이·청소년, 취미·실용·여행
        "reason": "사람들과의 조화와 현실적인 활동을 중시하며, 따뜻하고 다정한 스타일입니다."
    },
    "ISTP": {
        "categories": [5, 8],  # 과학·IT, 학습·참고서
        "reason": "도구적이고 분석적인 사고를 바탕으로 실험과 체계적 학습을 즐깁니다."
    },
    "ISFP": {
        "categories": [4, 6],  # 인문·사회, 어린이·청소년
        "reason": "감정적으로 따뜻하고 타인을 이해하는 데 강점이 있으며, 현실 기반의 지혜를 선호합니다."
    },
    "ESTP": {
        "categories": [2, 7],  # 경제·경영, 취미·실용·여행
        "reason": "도전적이고 현실적이며, 즉각적인 성과와 다양한 활동을 즐깁니다."
    },
    "ESFP": {
        "categories": [1, 8],  # 문학·에세이·만화, 학습·참고서
        "reason": "감각적이고 표현력이 풍부하여 예술적이면서도 현실적인 학습에 열정적입니다."
    }
    }

    mbti_info = mbti_map.get(mbti)
    if not mbti_info:
        return Response({"error": "올바른 MBTI 값을 입력해주세요."}, status=400)

    category_ids = mbti_info["categories"]

    # (향후 확장) Collaborative Filtering: MBTI 기반 좋아요 분석
    # from accounts.models import CustomUser
    # from django.db.models import Count
    # users_with_mbti = CustomUser.objects.filter(mbti=mbti)
    # if users_with_mbti.exists():
    #     liked_books = (
    #         Book.objects.filter(likes__in=users_with_mbti)
    #         .annotate(like_count=Count('likes'))
    #         .order_by('-like_count')
    #         .distinct()
    #     )
    #     if liked_books.count() >= 10:
    #         serializer = BookSerializer(liked_books[:12], many=True, context={"request": request})
    #         return Response(serializer.data)

    # 기본: Content-based (카테고리 기반 추천, 랜덤 5권)
    books = Book.objects.filter(category_id__in=category_ids).order_by('?')[:6]
    serializer = BookSerializer(books, many=True, context={"request": request})

    return Response({
        "mbti": mbti,
        "reason": mbti_info["reason"],
        "books": serializer.data
    })