# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Category
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class CustomUser(AbstractUser):
    # 사용자 성별을 선택할 수 있는 필드, 선택지로 '남성'과 '여성'을 제공
    GENDER_CHOICES = (
        ('M', '남성'),
        ('F', '여성'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )

    # 사용자 나이를 저장하는 필드, 선택 사항
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # 주간 평균 독서 시간을 분 단위로 저장하는 필드, 선택 사항
    weekly_reading_time = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # 연간 독서량(책 수)을 저장하는 필드, 선택 사항
    yearly_reading_volume = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # 사용자 프로필 이미지를 저장하는 필드, 업로드 시 300x300으로 리사이즈
    profile_image = ProcessedImageField(
        blank=True,
        null=True,
        upload_to='profile_image/%Y/%m',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 70},
        default='profile_image/default.png',
    )

    # 사용자가 관심 있는 장르를 다중 선택할 수 있도록 Category 모델과 M:N 관계 설정
    interested_genres = models.ManyToManyField(
        Category,
        blank=True,
        related_name="users",
    )

    # 사용자 간 팔로우 기능 구현을 위한 M:N 자기참조 관계 설정
    # symmetrical=False를 통해 단방향 관계로 설정
    followings = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    # 관리자 페이지 등에서 사용자 객체를 문자열로 표현할 때 username을 반환
    def __str__(self):
        return self.username
