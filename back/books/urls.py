# books/urls.py

from django.urls import path
from . import views

# books 앱의 API 엔드포인트 정의
urlpatterns = [
    # 전체 카테고리 목록 조회
    path('categories/', views.category_list),

    # 전체 도서 목록 조회 및 도서 등록 (GET, POST)
    path('', views.book_list_create),

    # 특정 도서 조회, 수정, 삭제 (GET, PUT/PATCH, DELETE)
    path('<int:book_id>/', views.book_detail_update_delete),

    # 위키피디아 API를 통한 저자 대표작 및 정보 가져오기
    path('<int:book_id>/works/', views.author_works_from_wiki),

    # TTS 음성 파일 재생성 요청
    path('<int:book_id>/tts/', views.regenerate_tts_audio),

    # 도서 좋아요/좋아요 취소 토글
    path('<int:book_id>/like/', views.toggle_book_like),

    # 사용자의 감상글 및 좋아요 기반 개인화 도서 추천
    path('recommend/personal/', views.personal_recommendation),

    # MBTI를 기반으로 도서 추천
    path('recommend/mbti/', views.mbti_book_recommendation),
]
