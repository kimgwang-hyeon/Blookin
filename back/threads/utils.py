# threads/utils.py

import requests
import openai
from pathlib import Path
from django.conf import settings
import uuid


# 감상글 제목, 본문, 도서 정보를 바탕으로 DALL·E 일러스트 이미지를 생성하는 함수
def generate_image_with_openai(thread_title, thread_content, book_title, book_author):
    # GPT에게 감성 키워드와 일러스트 스타일 프롬프트를 생성하도록 요청하는 입력 문장 구성
    keyword_extractor_prompt = f"""
    '{book_author}'의 책 '{book_title}'을 읽고 쓴 독서 다이어리의 감정과 분위기를 분석하여 키워드 5개를 추출하시오.
    추출한 키워드를 바탕으로, 감정을 시각적으로 표현할 수 있는 이미지 생성용 프롬프트를 작성하시오.

    생성될 이미지는 북카페나 그림책에서 볼 수 있는 따뜻하고 아기자기한 느낌의 일러스트여야 합니다.  
    부드러운 색감, 깔끔한 구성, 밝은 분위기를 가진 디지털 삽화 스타일로 묘사하십시오.

    <독서 다이어리>
        <제목>{thread_title}</제목>
        <본문>{thread_content}</본문>
    </독서 다이어리>

    <답변 예시>
        키워드: 따뜻함, 희망, 설렘, 고요함, 햇살
        프롬프트: '햇살 가득한 창가에서 따뜻한 차를 마시는 귀여운 일러스트, 밝은 파스텔톤, 텍스트 없음'
    """

    # OpenAI API 클라이언트 초기화
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        # GPT-4o-mini를 사용하여 프롬프트 생성 요청
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 감성 일러스트 AI 프롬프트 생성 전문가입니다."},
                {"role": "user", "content": keyword_extractor_prompt},
            ],
            max_tokens=2040,
            temperature=0.6
        )
        # 생성된 프롬프트 추출
        keyword_prompt = completion.choices[0].message.content.strip()
    except Exception as e:
        print("GPT 프롬프트 생성 실패:", e)
        return None

    # 텍스트나 기호를 제거하라는 조건 추가
    final_prompt = keyword_prompt + "\n텍스트, 숫자, 기호는 포함하지 마십시오."
    print("최종 이미지 프롬프트:", final_prompt)

    try:
        # DALL·E-3 모델을 이용하여 이미지 생성 요청
        response = client.images.generate(
            model="dall-e-3",
            prompt=final_prompt,
            size="1024x1024",  # 정사각형 비율
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
    except Exception as e:
        print("이미지 생성 실패:", e)
        return None

    try:
        # 생성된 이미지 URL에서 실제 이미지 파일 다운로드
        response_img = requests.get(image_url)
        if response_img.status_code == 200:
            output_dir = Path(settings.MEDIA_ROOT) / "thread_cover_img"
            output_dir.mkdir(parents=True, exist_ok=True)
            file_name = f"{uuid.uuid4()}.png"
            file_path = output_dir / file_name
            file_path.write_bytes(response_img.content)
            # 저장된 이미지 경로 반환 (MEDIA_URL 하위 상대경로)
            return str(Path("thread_cover_img") / file_name)
    except Exception as e:
        print("이미지 다운로드 실패:", e)

    return None
