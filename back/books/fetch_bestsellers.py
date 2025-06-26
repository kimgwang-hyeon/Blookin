# books/fetch_bestsellers_200.py

import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# 환경 변수 로드
load_dotenv()
TTB_KEY = os.getenv("ALADIN_TTB_KEY")

CATEGORY_MAPPING = {
    "소설": 1,
    "시": 1,
    "희곡": 1,
    "경제": 2,
    "경영": 2,
    "자기계발": 3,
    "자기 계발": 3,
    "인문": 4,
    "교양": 4,
    "취미": 5,
    "실용": 5,
    "어린이": 6,
    "청소년": 6,
    "과학": 7,
}

def map_category(category_name):
    for keyword, pk in CATEGORY_MAPPING.items():
        if keyword in category_name:
            return pk
    return None

def fetch_bestsellers_batch(start):
    url = "http://www.aladin.co.kr/ttb/api/ItemList.aspx"
    params = {
        "ttbkey": TTB_KEY,
        "QueryType": "Bestseller",
        "MaxResults": 50,
        "start": start,
        "SearchTarget": "Book",
        "output": "js",
        "Version": "20131101"
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json().get("item", [])

def convert_to_fixture(book_item):
    category_pk = map_category(book_item.get("categoryName", ""))
    if not category_pk:
        return None

    isbn = book_item.get("isbn13", "").strip()
    if not isbn:
        return None

    pub_date = book_item.get("pubDate", "")
    try:
        pub_date = datetime.strptime(pub_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except Exception:
        pub_date = "2000-01-01"

    return {
        "model": "books.book",
        "fields": {
            "category": category_pk,
            "title": book_item.get("title", "")[:200],
            "description": book_item.get("description", "")[:1000],
            "isbn": isbn,
            "cover": book_item.get("cover", ""),
            "publisher": book_item.get("publisher", ""),
            "pub_date": pub_date,
            "author": book_item.get("author", "")[:100],
            "author_info": "",
            "author_works": "",
            "customer_review_rank": float(book_item.get("customerReviewRank", 0)),
            "subTitle": book_item.get("subTitle", "")[:100],
        }
    }

def fetch_200_bestsellers():
    all_books = []
    seen_isbns = set()

    for start in [1, 51, 101, 151]:
        batch = fetch_bestsellers_batch(start)
        print(f"📦 {start}번부터 수집 중... {len(batch)}권")

        for item in batch:
            isbn = item.get("isbn13", "").strip()
            if not isbn or isbn in seen_isbns:
                continue
            seen_isbns.add(isbn)

            fixture = convert_to_fixture(item)
            if fixture:
                all_books.append(fixture)

            if len(all_books) >= 200:
                break

        if len(all_books) >= 200:
            break

    # 저장
    fixtures_path = Path(__file__).resolve().parent / "fixtures"
    fixtures_path.mkdir(parents=True, exist_ok=True)
    output_file = fixtures_path / "books_200.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_books, f, ensure_ascii=False, indent=2)

    print(f"✅ 저장 완료: {output_file} ({len(all_books)}권)")

if __name__ == "__main__":
    fetch_200_bestsellers()
