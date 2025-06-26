# books/recommender.py

from threads.models import Thread
from books.models import Book
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# 사용자가 좋아요한 도서를 기반으로 설명(description)의 유사도를 계산하여 추천
def recommend_by_description_similarity(user):
    # 사용자가 좋아요한 도서 목록 조회
    liked_books = user.liked_books.all()

    # 좋아요한 도서가 없다면 추천 불가
    if not liked_books.exists():
        return Book.objects.none()

    # description 필드가 존재하는 도서만 필터링
    books_with_desc = Book.objects.exclude(description__isnull=True).exclude(description__exact='')

    # 비교할 도서가 2권 미만이면 추천할 수 없음
    if books_with_desc.count() < 2:
        return Book.objects.none()

    # 도서 설명과 도서 ID 리스트 구성
    descriptions = [book.description for book in books_with_desc]
    book_ids = [book.id for book in books_with_desc]

    # 설명 벡터화 (TF-IDF)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(descriptions)

    # 좋아요한 책의 인덱스를 기준으로 유사도 계산
    liked_indices = [book_ids.index(book.id) for book in liked_books if book.id in book_ids]

    if not liked_indices:
        return Book.objects.none()

    # 전체 도서와 좋아요한 도서 간 유사도 평균 계산
    sim_scores = cosine_similarity(tfidf_matrix, tfidf_matrix[liked_indices]).mean(axis=1)

    # 유사도가 높은 순으로 정렬, 이미 좋아요한 도서는 제외
    sorted_indices = np.argsort(sim_scores)[::-1]
    recommended_ids = [
        book_ids[i] for i in sorted_indices
        if book_ids[i] not in [b.id for b in liked_books]
    ][:10]

    # 추천 도서 반환
    return Book.objects.filter(id__in=recommended_ids)


# 사용자가 작성한 감상글(Thread)에 기반한 도서 추천 함수
def recommend_by_threads_similarity(user):
    if not user.is_authenticated:
        return Book.objects.none()

    # 사용자가 작성한 감상글의 도서 ID 목록 추출
    thread_book_ids = Thread.objects.filter(user=user).values_list('book_id', flat=True)

    # description이 있는 도서만 대상으로 필터링
    books_with_desc = Book.objects.exclude(description__isnull=True).exclude(description__exact='')

    if books_with_desc.count() < 2:
        return Book.objects.none()

    # 설명과 도서 ID 리스트 구성
    descriptions = [book.description for book in books_with_desc]
    book_ids = [book.id for book in books_with_desc]

    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(descriptions)

    # 사용자가 작성한 감상글의 도서 인덱스 추출
    thread_indices = [book_ids.index(book_id) for book_id in thread_book_ids if book_id in book_ids]

    if not thread_indices:
        return Book.objects.none()

    # 유사도 계산 (전체 vs 감상글 작성 도서)
    sim_scores = cosine_similarity(tfidf_matrix, tfidf_matrix[thread_indices]).mean(axis=1)

    # 유사도 순으로 정렬 후 추천 (이미 작성한 도서 제외)
    sorted_indices = np.argsort(sim_scores)[::-1]
    recommended_ids = [
        book_ids[i] for i in sorted_indices
        if book_ids[i] not in thread_book_ids
    ][:10]

    # 추천 도서 반환
    return Book.objects.filter(id__in=recommended_ids)
