# 🚂 Railway 배포 가이드

> Sales Report Generator를 Railway에 배포하는 방법

---

## 📋 사전 준비

- [ ] GitHub 계정
- [ ] [Railway](https://railway.app) 계정 (GitHub 로그인)
- [ ] OpenAI API 키 (선택, 없으면 기본 통계만 생성)

---

## 🚀 배포 절차

### 1단계: GitHub에 코드 푸시

```bash
# Git 저장소가 없다면
git init
git add .
git commit -m "Initial commit - Sales Report Generator"

# GitHub에 새 저장소 생성 후
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2단계: Railway 프로젝트 생성

1. [railway.app](https://railway.app) 접속 후 로그인
2. **"New Project"** 클릭
3. **"Deploy from GitHub repo"** 선택
4. 저장소 연결 (필요 시 GitHub 권한 승인)
5. 배포할 저장소 선택

### 3단계: 환경 변수 설정

Railway 대시보드에서:

1. 배포된 서비스 클릭
2. **Variables** 탭 이동
3. **+ New Variable** 클릭 후 추가:

| 변수명 | 값 | 필수 |
|--------|-----|------|
| `OPENAI_API_KEY` | `sk-proj-...` (본인 API 키) | 선택* |
| `PORT` | (Railway가 자동 설정) | 불필요 |

> *API 키 없이도 기본 통계·차트는 생성됩니다. GPT AI 분석만 비활성화됩니다.

### 4단계: 도메인 설정 (공개 접속)

1. 서비스 **Settings** 탭
2. **Networking** → **Generate Domain** 클릭
3. 생성된 URL (예: `xxx.up.railway.app`)로 접속

---

## 📁 배포에 포함된 파일

| 파일 | 용도 |
|------|------|
| `Dockerfile` | Node.js + Python 컨테이너 빌드 |
| `.dockerignore` | 빌드 시 제외할 파일 |
| `.env.example` | 환경 변수 참고용 |

---

## 🔧 빌드 설정

Railway는 **Dockerfile**을 자동 감지하여 빌드합니다.

- **Base**: Node.js 20
- **추가**: Python 3, pip
- **의존성**: `npm ci` + `pip install -r requirements.txt`
- **시작**: `npm start`

---

## ⚠️ 문제 해결

### 빌드 실패: "python3: not found"
- Dockerfile에 Python 설치 단계가 포함되어 있습니다. 최신 Dockerfile 사용 여부 확인

### Matplotlib 오류 (display 관련)
- `MPLBACKEND=Agg`가 Dockerfile에 설정되어 있습니다

### 502 Bad Gateway
- 서버 시작 후 30초~1분 대기 (Python 패키지 로딩)
- Railway 로그에서 `Sales Report Generator Server is running` 메시지 확인

### API 키 오류
- Variables에 `OPENAI_API_KEY`가 정확히 입력되었는지 확인
- 공백이나 따옴표 없이 값만 입력

---

## 📊 비용

- **무료 크레딧**: 월 $5 (초기 검증에 충분)
- **사용량**: 빌드 시간 + 실행 시간 기준 과금
- [Railway 요금제](https://railway.app/pricing) 참고

---

## 🔄 재배포

GitHub에 Push하면 Railway가 자동으로 재배포합니다.

```bash
git add .
git commit -m "Update feature"
git push
```

---

*작성일: 2025-02-19*
