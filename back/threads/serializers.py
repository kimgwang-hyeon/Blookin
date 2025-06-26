# threads/serializers.py

from rest_framework import serializers
from .models import Thread, Comment
from books.models import Book, Category
from accounts.serializers import UserSimpleSerializer


# 카테고리 정보를 간단하게 직렬화하는 시리얼라이저 (id, name 등 포함)
class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# 도서 정보를 간단하게 직렬화하는 시리얼라이저
# 카테고리 정보는 중첩으로 출력됨
class BookSimpleSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


# 댓글 직렬화기
class CommentSerializer(serializers.ModelSerializer):
    # 작성자 정보는 문자열 형태로 출력 (기본적으로 __str__ 메서드 사용)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created_at', 'updated_at']


# 스레드(감상글) 직렬화기
class ThreadSerializer(serializers.ModelSerializer):
    # 글 등록 시 사용할 도서 ID (쓰기 전용)
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True
    )

    # 글 조회 시 출력할 도서 상세 정보 (읽기 전용)
    book_info = BookSimpleSerializer(source='book', read_only=True)

    # 작성자 정보 (UserSimpleSerializer로 중첩 직렬화)
    user_info = UserSimpleSerializer(source='user', read_only=True)

    # 좋아요 수 출력
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    # 연결된 댓글 목록 출력
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = [
            'id',             # 스레드 ID
            'title',          # 제목
            'content',        # 본문
            'reading_date',   # 독서 날짜
            'cover_img',      # 썸네일 이미지 경로
            'created_at',     # 생성일
            'updated_at',     # 수정일
            'book',           # 등록용 도서 ID
            'book_info',      # 응답용 도서 정보
            'user_info',      # 작성자 정보
            'likes_count',    # 좋아요 수
            'comments'        # 댓글 목록
        ]
