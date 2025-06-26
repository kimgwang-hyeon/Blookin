# books/serializers.py

from rest_framework import serializers
from .models import Book, Category
from threads.models import Thread
from threads.serializers import ThreadSerializer


# 카테고리 정보를 직렬화하는 시리얼라이저 (id와 name 필드만 포함)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# 도서 정보를 직렬화하는 시리얼라이저
class BookSerializer(serializers.ModelSerializer):
    # category 필드를 읽기 전용으로 표시하며, CategorySerializer로 중첩 직렬화
    category = CategorySerializer(read_only=True)

    # category_id는 쓰기 전용 필드이며 category 필드로 매핑됨
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    # 해당 도서에 연결된 감상글 목록을 ThreadSerializer로 출력 (읽기 전용)
    thread_set = ThreadSerializer(many=True, read_only=True)

    # 현재 요청한 사용자가 이 도서를 좋아요했는지 여부
    is_liked = serializers.SerializerMethodField()

    # 이 도서를 좋아요한 전체 사용자 수
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',                    # 도서 기본 키
            'title',                 # 도서 제목
            'subTitle',              # 도서 부제목
            'description',           # 도서 설명
            'isbn',                  # ISBN 번호
            'author',                # 저자 이름
            'publisher',             # 출판사 이름
            'pub_date',              # 출간일
            'cover',                 # 표지 이미지 URL
            'author_info',           # 저자 소개
            'author_works',          # 저자 대표작 목록
            'author_photo',          # 저자 사진 URL
            'tts_audio',             # TTS 음성 파일 경로
            'customer_review_rank',  # 사용자 리뷰 평점
            'category',              # 카테고리 전체 정보 (읽기 전용)
            'category_id',           # 카테고리 ID (쓰기 전용)
            'is_liked',              # 로그인 사용자가 좋아요했는지 여부
            'likes_count',           # 총 좋아요 수
            'page',                  # 페이지 수
            'thread_set',            # 감상글 목록
        ]

    # 현재 요청 유저가 이 도서를 좋아요했는지 확인
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.liked_users.filter(pk=user.pk).exists()
        return False

    # 좋아요한 사용자 수 반환
    def get_likes_count(self, obj):
        return obj.liked_users.count()
