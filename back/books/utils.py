# books/utils.py

import requests, json
from openai import OpenAI
from gtts import gTTS
from pathlib import Path
from django.conf import settings
import wikipediaapi
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

# 한국어 위키백과 접근 객체 생성
wiki = wikipediaapi.Wikipedia(language='ko', user_agent='BookAI/1.0')

# 작가 이름을 기반으로 작가 정보, 이미지 URL, 대표작 목록을 반환
def get_author_data(author):
    page = wiki.page(author)
    if page.exists():
        summary = page.summary
        img_url = get_wikipedia_image(author)
        major_works = extract_major_works_from_wikipedia(author)
        return summary, img_url, major_works

    # 위키백과에 정보가 없을 경우 GPT를 통해 정보 생성
    gpt_result = get_ai_summary_fallback(author)
    return gpt_result.get("author_info"), None, gpt_result.get("author_works", "").split(", ")

# 위키백과 API를 사용하여 작가의 대표 이미지 URL을 가져옴
def get_wikipedia_image(author):
    URL = "https://ko.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": author,
        "prop": "pageimages",
        "format": "json",
        "piprop": "original",
    }
    response = requests.get(URL, params=params)
    if response.ok:
        pages = response.json().get("query", {}).get("pages", {})
        for p in pages.values():
            return p.get("original", {}).get("source")
    return None

# 위키백과 HTML 파싱을 통해 대표작(《작품명》 형태)을 정규식으로 추출
def extract_major_works_from_wikipedia(author):
    encoded_author = quote(author)
    url = f"https://ko.wikipedia.org/wiki/{encoded_author}"
    try:
        res = requests.get(url, timeout=5)
        if not res.ok:
            return []
        soup = BeautifulSoup(res.text, "html.parser")
        target_area = soup.select_one(".infobox, .infobox-full-data") or soup
        text = target_area.get_text()
        works = re.findall(r'《(.*?)》', text)
        return list(set(works))
    except Exception as e:
        print(f"[extract_major_works_from_wikipedia 오류] {author}: {e}")
        return []

# GPT에게 직접 작가 정보 요약을 요청 (위키에 없을 경우 fallback)
def get_ai_summary_fallback(author):
    prompt = f"""
'{author}'라는 작가에 대해 아래 두 가지 정보를 요약하여 JSON 형식으로 작성하세요.

조건:
- 'author_info'는 해당 작가의 간단한 이력 및 배경 설명
- 'author_works'는 대표작 3~5편의 제목만 쉼표로 나열
- 작가가 존재하지 않거나 정보를 찾을 수 없다면 '정보 없음'이라고 답하세요.

응답 예시:
{{
  "author_info": "OO는 한국의 소설가로, ...",
  "author_works": "작품1, 작품2, 작품3"
}}
"""
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 작가 정보를 요약하는 도우미야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1024,
    )
    try:
        return json.loads(res.choices[0].message.content)
    except Exception:
        return {"author_info": "정보 없음", "author_works": "정보 없음"}

# 책 정보와 작가 정보를 바탕으로 작가 소개 및 대표작 목록을 GPT로부터 생성
def call_openai(book_title, author, wiki_summary, major_works=None):
    works_str = ", ".join(major_works) if major_works else "정보 없음"
    prompt = f"""
아래 도서 정보를 참고하여 작가에 대한 소개와 대표작 목록을 JSON으로 작성하세요.

책 제목: {book_title}
작가: {author}
위키 요약: {wiki_summary}
위키에서 수집한 대표작: {works_str}

조건:
- "author_info"는 작가에 대한 간단한 소개 문장입니다.
- "author_works"는 대표작 제목만 쉼표로 구분하여 나열합니다. 문장이 들어가면 안 됩니다.

예시 형식:
{{
  "author_info": "OO는 OOO 출신으로, 다수의 작품을 집필했다.",
  "author_works": "작품1, 작품2, 작품3"
}}
"""
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 작가 정보를 요약하고 대표작을 추천하는 도우미야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1024,
    )
    try:
        return json.loads(res.choices[0].message.content)
    except Exception:
        return {"author_info": "정보 없음", "author_works": "정보 없음"}

# 입력된 텍스트를 gTTS로 변환해 mp3 파일로 저장하고 경로 반환
def generate_tts_audio(book_id, text):
    path = Path(settings.MEDIA_ROOT) / "tts"
    path.mkdir(parents=True, exist_ok=True)
    file_path = path / f"tts_{book_id}.mp3"
    gTTS(text=text, lang='ko').save(str(file_path))
    return f"tts/tts_{book_id}.mp3"
