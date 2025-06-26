# accounts/urls.py

from django.urls import path
from .views import ProfileImageUploadView
from . import views
from django.conf import settings
from django.conf.urls.static import static

# accounts 앱의 사용자 관련 API URL 정의
urlpatterns = [
    # 특정 사용자의 프로필 정보 조회
    path('<str:user_login_id>/', views.user_profile),

    # 특정 사용자 계정 삭제
    path('<str:user_login_id>/delete/', views.user_delete),

    # 특정 사용자 팔로우/언팔로우 토글
    path('<str:user_login_id>/follow/', views.toggle_follow),

    # 특정 사용자 정보 수정
    path('<str:user_login_id>/edit/', views.update_user),

    # 프로필 이미지 업로드 전용 뷰
    path('user/', ProfileImageUploadView.as_view()),
]
