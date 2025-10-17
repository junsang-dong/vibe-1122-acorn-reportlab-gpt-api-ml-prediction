# ⚡ Quick Start Guide

## 3분 안에 시작하기!

### 📋 체크리스트

시작하기 전에 확인하세요:
- [ ] Node.js 설치됨 (v14+)
- [ ] Python 설치됨 (v3.8+)
- [ ] 터미널/명령 프롬프트 사용 가능
- [ ] OpenAI API 키 (선택사항)

---

## 🚀 3단계로 시작하기

### 1️⃣ 설치 (1분)

```bash
cd /Users/junsangdong/Desktop/vibe-1122-acorn-ml-prediction

# 자동 설치 (추천)
./start.sh

# 또는 수동 설치
npm install
pip3 install -r requirements.txt
```

### 2️⃣ 설정 (30초)

```bash
# .env 파일 생성 (선택사항)
echo "OPENAI_API_KEY=sk-..." > .env
echo "PORT=3000" >> .env
```

> 💡 OpenAI API 키가 없어도 기본 통계와 차트는 생성됩니다!

### 3️⃣ 실행 (10초)

```bash
npm start
```

브라우저에서 자동으로 열립니다: **http://localhost:3000**

---

## 📊 첫 번째 보고서 생성

### A. 웹 인터페이스 사용 (추천)

1. 🌐 브라우저에서 `http://localhost:3000` 접속
2. 📁 `Sample-100-Superstore.csv` 파일을 드래그 앤 드롭
3. 🚀 "리포트 생성" 버튼 클릭
4. ⏳ 15-20초 대기
5. 📄 PDF 자동 다운로드!

### B. 명령줄 사용

```bash
# 분석 테스트
python3 test_analysis.py

# API 직접 호출
curl -X POST http://localhost:3000/api/generate-report \
  -F "file=@Sample-100-Superstore.csv" \
  --output my-report.pdf
```

---

## 📁 내 데이터 사용하기

### 필수 컬럼

CSV 또는 XLSX 파일에 다음 컬럼이 있어야 합니다:

| 컬럼명 | 필수/선택 | 설명 |
|--------|-----------|------|
| `Sales` | **필수** | 매출 금액 |
| `Profit` | **필수** | 이익 금액 |
| `Category` | 권장 | 상품 카테고리 |
| `State` 또는 `Region` | 권장 | 지역 정보 |

### 파일 형식 예시

```csv
Sales,Profit,Category,State
261.96,41.91,Furniture,Kentucky
731.94,219.58,Furniture,California
14.62,6.87,Office Supplies,Texas
```

---

## 🎯 생성되는 내용

### PDF 보고서 포함 사항:

✅ **Executive Summary**
- 총 매출: $XXX,XXX
- 총 이익: $XX,XXX
- 이익률: XX.X%

✅ **6개 차트**
- 카테고리별 매출
- 지역별 이익
- 서브카테고리 매출
- 세그먼트 비교
- 매출-이익 상관관계
- 월별 추세

✅ **AI 분석 (GPT-4o)**
- 전문적인 비즈니스 인사이트
- 마케팅 전략 제안
- 실행 가능한 권장사항

---

## 🔧 일반적인 문제 해결

### 문제: `npm: command not found`
**해결:** Node.js를 설치하세요
```bash
# Mac (Homebrew)
brew install node

# 또는 https://nodejs.org 방문
```

### 문제: `python3: command not found`
**해결:** Python을 설치하세요
```bash
# Mac (Homebrew)
brew install python3

# 또는 https://www.python.org 방문
```

### 문제: 포트 3000이 이미 사용 중
**해결:** 다른 포트 사용
```bash
PORT=8080 npm start
```

### 문제: GPT 분석이 생성되지 않음
**해결:** 정상입니다! OpenAI API 키 없이도:
- ✅ 통계 분석 작동
- ✅ 차트 생성 작동
- ✅ PDF 생성 작동
- ❌ AI 텍스트 분석만 제외

---

## 📚 더 알아보기

### 상세 문서
- 📖 [README.md](./README.md) - 프로젝트 개요
- 🔧 [SETUP_GUIDE.md](./SETUP_GUIDE.md) - 상세 설치 가이드
- 📘 [USAGE_GUIDE.md](./USAGE_GUIDE.md) - 고급 사용법
- 🎯 [FEATURES.md](./FEATURES.md) - 모든 기능 설명
- 📊 [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - 프로젝트 요약

### 명령어 치트시트

```bash
# 서버 시작
npm start

# 개발 모드 (자동 재시작)
npm run dev

# 테스트
npm test
python3 test_analysis.py

# 전체 설정
npm run setup

# 서버 상태 확인
curl http://localhost:3000/api/health
```

---

## 💡 팁과 트릭

### 1. 빠른 테스트
```bash
# 샘플 데이터로 바로 테스트
python3 test_analysis.py
```

### 2. OpenAI API 키 얻기
1. https://platform.openai.com 방문
2. 계정 생성/로그인
3. API Keys → Create new key
4. `.env` 파일에 추가

### 3. 커스터마이징
- `analyze_sales.py`: 통계 수정
- `generate_pdf.py`: PDF 디자인 변경
- `public/styles.css`: 웹 디자인 수정

### 4. 배치 처리
```bash
# 여러 파일 자동 처리
for file in *.csv; do
    curl -X POST http://localhost:3000/api/generate-report \
      -F "file=@$file" -o "${file%.csv}.pdf"
done
```

---

## 🎉 성공!

축하합니다! 이제 다음을 할 수 있습니다:

✅ 판매 데이터 업로드  
✅ 자동 통계 분석  
✅ 전문 차트 생성  
✅ AI 인사이트 받기  
✅ PDF 보고서 다운로드  

---

## 🆘 도움이 필요하신가요?

### 빠른 도움말
1. ✅ 이 가이드 다시 읽기
2. ✅ 에러 메시지 확인
3. ✅ 서버 로그 보기
4. ✅ 테스트 스크립트 실행

### 추가 리소스
- 📖 전체 문서 읽기
- 🔍 에러 메시지 구글 검색
- 💬 GitHub Issues 확인

---

**지금 바로 시작하세요!**

```bash
./start.sh
```

**Happy Analyzing! 📊✨**

---

*작성 시간: 5분*  
*실행 시간: 3분*  
*첫 보고서: 20초*  

**총 소요 시간: 10분 이내!** ⚡

