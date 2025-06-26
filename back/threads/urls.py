# threads/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# threads 앱의 URL 경로 설정
urlpatterns = [
    # 감상글 목록 조회 및 감상글 작성
    path('', views.thread_list_create, name='thread_list_create'),

    # 감상글 상세 조회, 수정, 삭제
    path('<int:thread_id>/', views.thread_detail, name='thread_detail'),

    # 감상글 좋아요 토글
    path('<int:thread_id>/like/', views.thread_like_toggle, name='thread_like_toggle'),

    # 댓글 생성 (특정 스레드에 대해)
    path('<int:thread_id>/comments/', views.comment_create, name='comment_create'),

    # 댓글 삭제 (댓글 ID 기준)
    path('comments/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]

# 미디어 파일 경로 설정 (커버 이미지 등 제공)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
