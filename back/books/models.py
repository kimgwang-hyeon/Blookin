# books/models.py

from django.db import models
from django.conf import settings


# 도서 장르를 나타내는 모델
class Category(models.Model):
    # 카테고리 이름 필드 (예: 소설, 자기계발, 과학 등)
    name = models.CharField(max_length=50)

    # 관리자 페이지 등에서 카테고리 이름 출력
    def __str__(self):
        return self.name


# 개별 도서를 나타내는 모델
class Book(models.Model):
    # 도서가 속한 카테고리, 카테고리가 삭제되더라도 도서는 삭제되지 않도록 보호
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='books'
    )

    # 도서 제목
    title = models.CharField(max_length=200)

    # 도서 설명 또는 줄거리
    description = models.TextField()

    # ISBN 번호 (일반적으로 13자리 문자열)
    isbn = models.CharField(max_length=20)

    # 도서 표지 이미지 URL
    cover = models.URLField()

    # 출판사 이름
    publisher = models.CharField(max_length=100)

    # 페이지 수 (선택 입력)
    page = models.IntegerField(null=True, blank=True)

    # 출간일
    pub_date = models.DateField()

    # 저자 이름
    author = models.CharField(max_length=100)

    # 저자 소개 (GPT 또는 위키피디아 기반)
    author_info = models.TextField()

    # 저자 사진 URL (선택 입력)
    author_photo = models.URLField(null=True, blank=True)

    # 저자의 대표작 목록 (쉼표 구분 문자열 또는 JSON 문자열, 선택 입력)
    author_works = models.TextField(null=True, blank=True)

    # 도서 설명을 TTS로 생성한 음성 파일 (선택 입력)
    tts_audio = models.FileField(upload_to="tts/", null=True, blank=True)

    # 알라딘 등에서 가져온 도서 평점 (실수형)
    customer_review_rank = models.FloatField()

    # 도서의 부제목
    subTitle = models.CharField(max_length=100)

    # 도서에 좋아요를 누른 사용자 목록 (ManyToMany 관계)
    liked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_books',
        blank=True
    )

    # 관리자 페이지 등에서 도서 제목이 출력되도록 설정
    def __str__(self):
        return self.title