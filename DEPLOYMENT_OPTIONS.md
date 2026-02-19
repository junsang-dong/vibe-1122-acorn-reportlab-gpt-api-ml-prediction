# 🚀 Sales Report Generator - 초기 사용자 검증용 배포 가이드

> 현재 앱 구조: **Node.js (Express) + Python (subprocess)** 하이브리드 아키텍처

---

## 📋 배포 전 체크리스트

| 항목 | 현재 상태 |
|------|----------|
| 처리 시간 | 15~20초 (서버리스 타임아웃 주의) |
| 파일 시스템 | uploads, temp_charts, output 디렉토리 필요 |
| 환경 변수 | OPENAI_API_KEY 필수 |
| 런타임 | Node.js + Python 3.8+ 동시 필요 |

---

## 🏆 추천 순위 (초기 검증용)

### 1순위: **Railway** ⭐ 가장 추천

**적합한 이유**
- ✅ **현재 아키텍처 그대로 배포** 가능 (코드 수정 최소)
- ✅ Node.js + Python 동시 지원 (Nixpacks 자동 감지)
- ✅ 파일 시스템(임시 스토리지) 제공
- ✅ 월 $5 무료 크레딧 (초기 검증에 충분)
- ✅ GitHub 연동 → Push 시 자동 배포
- ✅ 환경 변수(.env) 쉬운 설정

**배포 절차**
1. [railway.app](https://railway.app) 가입
2. "New Project" → "Deploy from GitHub" 선택
3. 저장소 연결 후 자동 빌드
4. Variables에 `OPENAI_API_KEY` 추가
5. `nixpacks.toml` 또는 `Procfile`로 시작 명령 지정

**필요 파일 예시 (nixpacks.toml)**
```toml
[phases.setup]
nixPkgs = ["nodejs_20", "python311"]

[phases.install]
cmds = ["npm install", "pip install -r requirements.txt"]

[start]
cmd = "npm start"
```

---

### 2순위: **Render**

**적합한 이유**
- ✅ 무료 티어 (월 750시간)
- ✅ Node.js + Python 빌드팩 지원
- ✅ GitHub 자동 배포
- ⚠️ 무료 플랜: 15분 비활성 시 스핀다운 → 콜드스타트 30초~1분

**배포 절차**
1. [render.com](https://render.com) 가입
2. "New" → "Web Service"
3. GitHub 저장소 연결
4. Build Command: `npm install && pip install -r requirements.txt`
5. Start Command: `npm start`
6. Environment: `OPENAI_API_KEY` 추가

**주의**: 무료 플랜은 인스턴스가 sleep 상태가 되므로, 첫 요청 시 지연이 발생할 수 있음.

---

### 3순위: **Replit**

**적합한 이유**
- ✅ 브라우저에서 바로 개발 + 배포
- ✅ Node + Python 동시 실행 환경
- ✅ 무료 플랜으로 데모/검증 가능
- ✅ 링크 하나로 공유 가능
- ⚠️ 무료: Sleep 모드 있음

**배포 절차**
1. [replit.com](https://replit.com) 가입
2. "Create Repl" → "Import from GitHub"
3. 저장소 URL 입력
4. .env에 OPENAI_API_KEY 설정 (Secrets)
5. Run 클릭 → 자동으로 URL 생성

---

### 4순위: **Streamlit** (리팩토링 필요)

**적합한 이유**
- ✅ Streamlit Cloud **완전 무료**
- ✅ 데이터 앱에 최적화된 UX
- ✅ Hugging Face Spaces 대안
- ❌ **전체 앱을 Python/Streamlit으로 재작성** 필요

**현재 구조와의 차이**
| 현재 | Streamlit 전환 시 |
|------|------------------|
| Express + HTML/CSS/JS | Streamlit (Python만) |
| Multer 파일 업로드 | st.file_uploader |
| Fetch API | st.session_state |
| PDF 다운로드 | st.download_button |

**예상 작업량**: 2~4시간 (analyze_sales, generate_gpt_report, generate_pdf 로직 재사용 가능)

**Streamlit 앱 예시 구조**
```python
# app_streamlit.py
import streamlit as st
import pandas as pd
# ... (기존 Python 모듈 import)

st.title("📊 Sales Report Generator")
uploaded_file = st.file_uploader("CSV/XLSX 업로드", type=["csv", "xlsx"])
if uploaded_file and st.button("리포트 생성"):
    with st.spinner("분석 중..."):
        stats = analyze(uploaded_file)
        analysis = generate_gpt(stats)
        pdf_bytes = generate_pdf(stats, analysis)
    st.download_button("PDF 다운로드", pdf_bytes, "report.pdf")
```

---

### 5순위: **Vercel** ⚠️ 제한적

**부적합한 이유**
- ❌ Serverless 함수: **실행 시간 제한** (Hobby 10초, Pro 60초)
- ❌ 15~20초 처리 → Hobby 플랜에서 타임아웃 가능성
- ❌ Node에서 Python subprocess 호출 구조가 Serverless에 맞지 않음
- ❌ `/tmp`만 사용 가능 (512MB), 영구 스토리지 없음

**가능하게 하려면**
- API를 여러 단계로 분리 (분석 → GPT → PDF)하고 각각 별도 함수로 구성
- 또는 Vercel 대신 **Vercel + 외부 Python API** (Railway 등) 조합

---

### 6순위: **Fly.io**

**적합한 이유**
- ✅ Docker 기반으로 Node + Python 자유롭게 구성
- ✅ 글로벌 엣지 배포
- ✅ 무료 티어 (제한적)

**배포 절차**
1. Dockerfile 작성 (Node + Python 멀티스테이지 또는 단일 이미지)
2. `fly launch` → `fly deploy`

**Dockerfile 예시**
```dockerfile
FROM node:20-slim
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["npm", "start"]
```

---

## 📊 옵션 비교표

| 플랫폼 | 코드 수정 | 무료 티어 | 설정 난이도 | 초기 검증 적합도 |
|--------|----------|----------|-------------|------------------|
| **Railway** | 최소 | $5/월 크레딧 | ⭐ 쉬움 | ⭐⭐⭐⭐⭐ |
| **Render** | 최소 | 750h/월 | ⭐ 쉬움 | ⭐⭐⭐⭐ |
| **Replit** | 최소 | 있음 (Sleep) | ⭐ 매우 쉬움 | ⭐⭐⭐⭐ |
| **Streamlit** | 전체 재작성 | 무제한 | ⭐⭐ 보통 | ⭐⭐⭐ |
| **Vercel** | 대규모 리팩토링 | 있음 | ⭐⭐ | ⭐ |
| **Fly.io** | Dockerfile 추가 | 제한적 | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 최종 권장안

### 초기 사용자 검증 (1~2주)
→ **Railway** 또는 **Render** 선택

- 코드 변경 최소
- GitHub Push만으로 배포
- 무료/저비용으로 충분한 트래픽 처리

### 빠른 데모/피칭 (당일)
→ **Replit**

- 계정 생성 후 GitHub Import
- 5분 내 배포 완료
- 링크 공유로 즉시 시연 가능

### 장기적으로 Streamlit 전환 검토
- 사용자 피드백 후 "데이터 앱" 특화 필요 시
- Streamlit Cloud 무료 + Hugging Face Spaces 연동 가능

---

## 📁 배포 시 추가로 준비할 파일

### 1. `nixpacks.toml` (Railway용)
```toml
[phases.setup]
nixPkgs = ["nodejs_20", "python311"]

[phases.install]
cmds = ["npm install", "pip install -r requirements.txt"]

[start]
cmd = "npm start"
```

### 2. `Procfile` (Render/Heroku용)
```
web: npm start
```

### 3. `runtime.txt` (Python 버전 명시, 필요시)
```
python-3.11.0
```

---

*작성일: 2025-02-19*
