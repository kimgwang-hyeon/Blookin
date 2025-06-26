# blookin/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Django 관리자 페이지 URL
    path("admin/", admin.site.urls),

    # 로그인, 로그아웃, 비밀번호 변경 등 dj-rest-auth 기본 인증 API
    path('api/accounts/', include('dj_rest_auth.urls')),

    # 회원가입 관련 API (dj-rest-auth의 registration 확장)
    path('api/accounts/signup/', include('dj_rest_auth.registration.urls')),

    # 사용자 관련 커스텀 API (프로필 조회, 수정, 탈퇴 등)
    path('api/accounts/', include('accounts.urls')),

    # 도서 관련 API 엔드포인트
    path("api/books/", include("books.urls")),

    # 쓰레드(감상글) 관련 API 엔드포인트
    path("api/threads/", include("threads.urls")),
]

# 미디어 파일 URL 설정 (프로필 이미지 등 정적 파일 제공)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
