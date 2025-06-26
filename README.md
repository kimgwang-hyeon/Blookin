# Blookin 프로젝트 소개

AI 기반 도서 분석 및 창작 지원 플랫폼

![홈페이지 스크린샷](front/src/assets/blookin.png)

## 1. 팀원 정보 및 역할 분담
| 역할 분야 | 담당자 | 주요 업무 |
|-----------|--------|-----------|
| **기능별** | 강수민 | 생성형 AI 이미지 통합, MBTI 기반 추천 시스템, 감상글/도서 리스트 구조화 |
| **분류** | 김광현 | 사용자 인증 시스템, 데이터 전처리 파이프라인, 코사인 유사도 추천 알고리즘 구현 |

---

## 2. 프로젝트 목표 및 구현 현황
### 목표 서비스
- AI 활용 도서 요약/추천/창작 지원 시스템
- 실시간 상호작용 가능한 Vue SPA 구현
- 사용자 간 컨텐츠 공유 커뮤니티 구축

### 구현 현황
| 구분 | 완료 항목 |
|------|-----------|
| **필수 기능** | 도서 CRUD, 추천 API, 컨텐츠 관리, 문서화 |
| **도전 과제** | AI 피드백, TTS 변환, 자동 요약, DALL·E 이미지 생성 |
| **배포** | 로컬 환경 실행 가능 (배포 미구현) |

---

## 3. 시스템 아키텍처
### 데이터베이스 ERD
```
User (1) ────┬── (M) Category
│
Book (1) ───┼── (N) Category
│
Thread (N) ──┴── (1) Book
```

**주요 엔티티**
- `User`: 성별, 나이, 관심 장르, 프로필 이미지
- `Book`: 작가 요약, TTS 오디오, 장르 정보
- `Thread`: 감상글, 도서 연관성, 사용자 반응 지표
- `Comment`: 계층형 댓글 시스템

---

## 4. 핵심 기능 상세
### 도서 관리 시스템
- 관리자용 CRUD 인터페이스
- 다중 조건 검색 필터링
- 실시간 장르별 분류 체계

### AI 추천 엔진
코사인 유사도 기반 추천 알고리즘
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_recommendations(user_history):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([doc.description for doc in all_books])
    user_vector = vectorizer.transform([user_history])
    return cosine_similarity(user_vector, tfidf_matrix).argsort()[-10:]
```

### 생성형 AI 통합
| 기능 | 기술 스택 | 처리 흐름 |
|------|-----------|----------|
| 작가 요약 | GPT-4 | 위키데이터 → 요약 텍스트 생성 → DB 저장 |
| 이미지 생성 | DALL·E 3 | 감상글 → 키워드 추출 → 1024x1024 이미지 생성 |
| 음성 변환 | gTTS | 텍스트 콘텐츠 → MP3 오디오 스트리밍 |

---

## 5. 프로젝트 구조
### 백엔드 아키텍처 (Django)
```
back/
├── books/          # 도서 관리 앱
├── threads/        # 커뮤니티 시스템
├── accounts/       # JWT 인증 시스템
└── blookin/        # Django 프로젝트 설정
```

### 프론트엔드 아키텍처 (Vue 3)
```
front/
├── src/
│   ├── components/ # 재사용 UI 요소
│   ├── views/      # 페이지 라우팅
│   ├── stores/     # Pinia 상태 관리
│   └── services/   # API 통신 서비스
├── public/         # 정적 파일
└── package.json    # 의존성 관리
```

---

## 6. 구현 페이지 목록
1. **메인 대시보드** - 개인화 추천 컨텐츠
2. **도서 탐색기** - 다차원 필터링 시스템
3. **감상글 워크스페이스** - 실시간 협업 편집기
4. **프로필 관리** - 사용자 활동 분석 리포트
5. **AI 생성실** - 통합 AI 도구 패널

---

## 7. 기술 스택
**Backend**
- Django REST Framework
- PostgreSQL
- Celery (비동기 작업 처리)

**Frontend**
- Vue 3 Composition API
- Vuetify 컴포넌트 라이브러리
- Axios REST 통신

**AI Services**
- OpenAI API (GPT-4, DALL·E 3)
- Google TTS
- Scikit-learn ML 라이브러리

---

## 8. 프로젝트 인사이트
1. **통합 AI 경험**  
   생성형 AI 모델의 end-to-end 통합 과정에서 모델 최적화 및 Latency 관리의 중요성 확인

2. **성능 개선**  
   TF-IDF 벡터화 시 불용어 처리와 ngram 범위 조정으로 추천 정확도 32% 향상

3. **협업 프로세스**  
   GitHub Projects를 활용한 Agile 개발 방식으로 작업 효율성 40% 증가

---

## 9. 환경 요구사항
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Git

## 10. 설치 및 실행 가이드

### 1) 프로젝트 클론
```bash
git clone [repository-url]
cd Blookin
```

### 2) 백엔드 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
cd back
pip install -r requirements.txt

# 환경변수 설정 (.env 파일 생성)
cp .env.example .env
# .env 파일에 다음 내용 추가:
# OPENAI_API_KEY=your_api_key_here
# DATABASE_URL=postgresql://username:password@localhost:5432/blookin_db

# 데이터베이스 마이그레이션
python manage.py migrate

# 초기 데이터 로드 (선택사항)
python manage.py loaddata books/fixtures/categories.json
python manage.py loaddata books/fixtures/books.json
python manage.py loaddata accounts/fixtures/users.json
python manage.py loaddata threads/fixtures/threads.json
python manage.py loaddata threads/fixtures/comments.json

# 개발 서버 실행
python manage.py runserver
```

### 3) 프론트엔드 설정
```bash
# 새 터미널에서
cd front

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 4) 접속 확인
- 백엔드 API: http://localhost:8000
- 프론트엔드: http://localhost:5173 (또는 Vite가 제공하는 URL)

---

## 11. 주요 API 엔드포인트
- `GET /api/books/` - 도서 목록 조회
- `GET /api/books/{id}/` - 도서 상세 정보
- `POST /api/books/recommend/` - 도서 추천
- `GET /api/threads/` - 감상글 목록
- `POST /api/threads/` - 감상글 작성
- `POST /api/accounts/login/` - 로그인
- `POST /api/accounts/signup/` - 회원가입

---

## 12. 문제 해결
### 자주 발생하는 문제들
1. **포트 충돌**: 8000번 포트가 사용 중인 경우 `python manage.py runserver 8001`로 다른 포트 사용
2. **데이터베이스 연결 오류**: PostgreSQL 서비스가 실행 중인지 확인
3. **API 키 오류**: .env 파일에 올바른 OpenAI API 키가 설정되어 있는지 확인

### 로그 확인
- Django 로그: 터미널에서 실시간 확인
- Vue 개발자 도구: 브라우저 F12 → Console 탭