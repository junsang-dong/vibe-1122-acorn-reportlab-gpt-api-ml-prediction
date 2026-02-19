# 📊 Sales Report Generator

> **AI 기반 자동 매출 리포트 생성 시스템**

Pandas와 GPT API를 활용하여 판매 데이터를 분석하고, 전문적인 PDF 보고서를 자동으로 생성하는 풀스택 웹 애플리케이션입니다.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-14+-green.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| 📁 **파일 업로드** | CSV/XLSX 파일 드래그 앤 드롭 또는 선택 |
| 📊 **데이터 분석** | Pandas로 통계 자동 계산 (총매출, 평균, 카테고리별 합계 등) |
| 🤖 **AI 분석** | GPT-4o를 통한 자연어 비즈니스 보고서 생성 |
| 📈 **시각화** | Matplotlib로 6가지 전문 차트 자동 생성 |
| 📄 **PDF 생성** | ReportLab으로 통계, 차트, AI 분석을 포함한 PDF 생성 |
| ⚡ **즉시 다운로드** | 브라우저에서 완성된 보고서 자동 다운로드 |

---

## 🎯 데모

### 입력
```csv
Sales,Profit,Category,State,Order Date
261.96,41.91,Furniture,Kentucky,11/8/2016
731.94,219.58,Furniture,California,11/8/2016
14.62,6.87,Office Supplies,Texas,6/12/2016
```

### 출력
✅ 20페이지 전문 PDF 보고서  
✅ Executive Summary + 통계 테이블  
✅ 6개 고해상도 차트  
✅ GPT-4o 생성 AI 분석 및 전략 제안  

**처리 시간: 약 15-20초** ⚡

---

## 🚀 빠른 시작

### ⚡ 자동 설치 (권장)

```bash
# 모든 의존성 설치 및 서버 시작
./start.sh
```

### 🔧 수동 설치

**1. Python 패키지 설치**
```bash
pip3 install -r requirements.txt
```

**2. Node.js 패키지 설치**
```bash
npm install
```

**3. 환경 변수 설정**
```bash
# .env 파일 생성
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
echo "PORT=8080" >> .env
```

> 💡 **팁**: OpenAI API 키가 없어도 기본 통계와 차트는 생성됩니다!

**4. 서버 시작**
```bash
npm start
```

**5. 브라우저 접속**
```
http://localhost:8080
```

---

## 📖 상세 문서

| 문서 | 내용 |
|------|------|
| 🚂 [RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md) | Railway 클라우드 배포 가이드 |
| 📘 [QUICK_START.md](./QUICK_START.md) | 3분 안에 시작하기 |
| 🔧 [SETUP_GUIDE.md](./SETUP_GUIDE.md) | 상세 설치 및 문제 해결 |
| 📗 [USAGE_GUIDE.md](./USAGE_GUIDE.md) | 고급 사용법 및 커스터마이징 |
| 🎯 [FEATURES.md](./FEATURES.md) | 모든 기능 상세 설명 |
| 📊 [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) | 프로젝트 전체 요약 |

---

## 💻 사용 방법

### 웹 인터페이스

1. 🌐 **브라우저 접속**: `http://localhost:8080`
2. 📁 **파일 업로드**: CSV/XLSX 파일을 드래그 앤 드롭
3. 🚀 **리포트 생성**: "리포트 생성" 버튼 클릭
4. ⏳ **대기**: 15-20초 (진행 상황 실시간 표시)
5. 📄 **다운로드**: PDF 자동 다운로드 완료!

### 명령줄 인터페이스

```bash
# 샘플 데이터로 테스트
python3 test_analysis.py

# API 직접 호출
curl -X POST http://localhost:8080/api/generate-report \
  -F "file=@Sample-100-Superstore.csv" \
  --output report.pdf
```

---

## 📁 데이터 요구사항

### 필수 컬럼

| 컬럼명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `Sales` | 숫자 | 매출 금액 | 261.96 |
| `Profit` | 숫자 | 이익 금액 | 41.91 |

### 권장 컬럼 (더 상세한 분석)

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `Category` | 텍스트 | 상품 카테고리 |
| `Sub-Category` | 텍스트 | 세부 카테고리 |
| `State` 또는 `Region` | 텍스트 | 지역 정보 |
| `Segment` | 텍스트 | 고객 세그먼트 |
| `Order Date` | 날짜 | 주문 날짜 |
| `Quantity` | 숫자 | 판매 수량 |

**예시 파일**: [`Sample-100-Superstore.csv`](./Sample-100-Superstore.csv)

---

## 🛠️ 기술 스택

### Backend
- **Node.js** (v14+) - JavaScript 런타임
- **Express.js** (v4.18) - 웹 서버 프레임워크
- **Python** (v3.8+) - 데이터 분석 엔진

### Data Analysis & Visualization
- **Pandas** (v2.1.4) - 데이터 분석
- **NumPy** (v1.26.2) - 수치 계산
- **Matplotlib** (v3.8.2) - 데이터 시각화
- **Seaborn** (v0.13.0) - 통계 시각화

### AI & Document Generation
- **OpenAI API** (GPT-4o) - 자연어 분석 생성
- **ReportLab** (v4.0.7) - PDF 생성
- **Pillow** (v10.1.0) - 이미지 처리

### Frontend
- **HTML5 + CSS3** - 모던 UI/UX
- **JavaScript** - 클라이언트 로직
- **Responsive Design** - 모바일/태블릿 지원

---

## 📊 생성되는 보고서 내용

### 1. Executive Summary
- 총 매출, 이익, 이익률
- 평균 매출 및 이익
- 총 주문 수

### 2. 통계 테이블
- 카테고리별 성과
- 지역별 매출 및 이익
- 세그먼트별 분석

### 3. 데이터 시각화 (6개 차트)
1. **카테고리별 매출** - 가로 막대 차트
2. **지역별 이익** - 색상 구분 막대 차트
3. **서브카테고리 매출** - 세로 막대 차트
4. **세그먼트 비교** - 그룹 막대 차트
5. **매출-이익 상관관계** - 산점도
6. **월별 매출 추세** - 선 그래프

### 4. AI 생성 분석 (GPT-4o)
- 전체 개요 (Executive Summary)
- 주요 발견 사항 (Key Findings)
- 카테고리/지역/세그먼트 상세 분석
- 개선 제안 및 마케팅 전략
- 결론 및 다음 단계

---

## 🎨 스크린샷

### 웹 인터페이스
```
┌─────────────────────────────────────────────┐
│     📊 Sales Report Generator               │
│     AI 기반 매출 분석 및 리포트 자동 생성    │
├─────────────────────────────────────────────┤
│                                              │
│  [📁 파일 업로드 영역]                       │
│   드래그 앤 드롭 또는 클릭하여 선택          │
│                                              │
│  [🚀 리포트 생성]                            │
│                                              │
│  ━━━━━━━━━━━━━━━━ 80% ━━━━━━━━━━━━━━━━     │
│  Matplotlib 차트 생성 중...                  │
│                                              │
└─────────────────────────────────────────────┘
```

---

## 🧪 테스트

```bash
# 분석 기능 테스트
npm test
# 또는
python3 test_analysis.py

# 서버 상태 확인
curl http://localhost:8080/api/health
```

---

## 📈 성능

| 파일 크기 | 행 수 | 처리 시간 |
|-----------|-------|-----------|
| 소규모 | < 1,000 | ~10-15초 |
| 중규모 | 1,000-10,000 | ~15-25초 |
| 대규모 | 10,000+ | ~25-40초 |

---

## 🔒 보안

- ✅ 파일 형식 검증 (.csv, .xlsx, .xls만)
- ✅ 파일 크기 제한 (10MB)
- ✅ 자동 파일 정리 (60초 후)
- ✅ 환경 변수로 API 키 관리
- ✅ CORS 설정

## 🔤 한글 지원

- ✅ **ReportLab 한글 폰트 자동 등록** (AppleGothic, Nanum Gothic 등)
- ✅ **Matplotlib 한글 폰트 자동 설정** (크로스 플랫폼 지원)
- ✅ **완벽한 한글 텍스트 표시** (AI 분석, 차트 제목, 통계 등)
- ✅ **폰트 폴백 시스템** (한글 폰트 없을 시 기본 폰트 사용)

---

## 🤝 기여

기여를 환영합니다! 다음 방법으로 참여할 수 있습니다:

1. Fork 프로젝트
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

---

## 🙏 감사의 글

- [Pandas](https://pandas.pydata.org/) - 데이터 분석 라이브러리
- [Matplotlib](https://matplotlib.org/) - 시각화 라이브러리
- [ReportLab](https://www.reportlab.com/) - PDF 생성 라이브러리
- [OpenAI](https://openai.com/) - GPT API 제공

---

## 📞 지원

- 📖 **문서**: [상세 가이드 모음](./QUICK_START.md)
- 🐛 **버그 리포트**: GitHub Issues
- 💬 **질문**: Discussions

---

## 🎉 시작하기

```bash
# 한 줄로 시작!
./start.sh && open http://localhost:8080
```

**Happy Analyzing! 📊✨**

---

*Created with ❤️ using Python, Node.js, and AI*

*Powered by Pandas, Matplotlib, OpenAI GPT, and ReportLab*

