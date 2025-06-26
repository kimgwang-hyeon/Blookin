# threads/models.py

import datetime
from django.db import models
from django.conf import settings


# 감상글(스레드) 모델 정의
class Thread(models.Model):
    # 글 제목
    title = models.CharField(max_length=100)

    # 글 본문 (독서 후 감상)
    content = models.TextField()

    # 책을 읽은 날짜 (기본값은 오늘 날짜)
    reading_date = models.DateField(default=datetime.date.today)

    # AI로 생성된 썸네일 이미지 (선택 입력)
    cover_img = models.ImageField(upload_to="thread_cover_img/", blank=True)

    # 생성 시각 (자동 저장)
    created_at = models.DateTimeField(auto_now_add=True)

    # 수정 시각 (자동 업데이트)
    updated_at = models.DateTimeField(auto_now=True)

    # 이 글이 작성된 도서 (Book 모델과의 관계)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)

    # 글 작성자 (사용자 모델과의 관계)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 이 글에 좋아요를 누른 사용자 목록 (ManyToManyField)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_threads",
        blank=True
    )

    # 객체 문자열 표현 (작성자 + 제목 + 도서 제목)
    def __str__(self):
        return f"[{self.user.username}] {self.title} ({self.book.title})"

    # 기본 정렬 기준: 생성일 내림차순 (최신순)
    class Meta:
        ordering = ['-created_at']


# 댓글 모델 정의
class Comment(models.Model):
    # 댓글 본문 (최대 100자)
    content = models.CharField(max_length=100)

    # 연결된 스레드 (Thread 모델과의 관계)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')

    # 댓글 작성자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 댓글 생성 시각 (자동 저장)
    created_at = models.DateTimeField(auto_now_add=True)

    # 댓글 수정 시각 (자동 업데이트)
    updated_at = models.DateTimeField(auto_now=True)

    # 객체 문자열 표현 (작성자 + 댓글 내용 앞부분)
    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

    # 기본 정렬 기준: 생성일 내림차순 (최신순)
    class Meta:
        ordering = ['-created_at']
