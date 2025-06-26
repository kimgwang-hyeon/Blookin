# threads/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count

from .models import Thread, Comment
from .serializers import ThreadSerializer, CommentSerializer
from .utils import generate_image_with_openai


# 감상글(스레드) 목록 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def thread_list_create(request):
    if request.method == 'GET':
        # 쿼리 파라미터 수집
        query = request.GET.get('q')
        category_id = request.GET.get('category')
        ordering = request.GET.get('ordering', '-created_at')

        # 좋아요 수 계산 포함 쿼리셋
        threads = Thread.objects.all().annotate(likes_count=Count('likes'))

        # 검색어 필터
        if query:
            threads = threads.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(book__title__icontains=query) |
                Q(book__author__icontains=query)
            ).distinct()

        # 카테고리 필터
        if category_id:
            threads = threads.filter(book__category_id=category_id)

        threads = threads.order_by(ordering)

        # 직렬화 후 응답
        serializer = ThreadSerializer(threads, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        # 감상글 작성 요청
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            thread = serializer.save(user=request.user)

            # AI 커버 이미지 생성
            book = thread.book
            image_path = generate_image_with_openai(
                thread.title, thread.content, book.title, book.author
            )
            if image_path:
                thread.cover_img = image_path
                thread.save()

            return Response(ThreadSerializer(thread).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 단일 감상글 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def thread_detail(request, thread_id):
    try:
        thread = Thread.objects.get(pk=thread_id)
    except Thread.DoesNotExist:
        return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # 작성자만 수정 가능
        if thread.user != request.user:
            return Response({'error': '권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ThreadSerializer(thread, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # 작성자만 삭제 가능
        if thread.user != request.user:
            return Response({'error': '권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 감상글 좋아요/취소 토글
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def thread_like_toggle(request, thread_id):
    try:
        thread = Thread.objects.get(pk=thread_id)
    except Thread.DoesNotExist:
        return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if thread.likes.filter(pk=user.pk).exists():
        thread.likes.remove(user)
        liked = False
    else:
        thread.likes.add(user)
        liked = True

    return Response({'liked': liked, 'likes_count': thread.likes.count()})


# 댓글 생성 (해당 감상글에 대해)
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_create(request, thread_id):
    try:
        thread = Thread.objects.get(pk=thread_id)
    except Thread.DoesNotExist:
        return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, thread=thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_delete(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    # 작성자만 삭제 가능
    if comment.user != request.user:
        return Response({'error': '권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
