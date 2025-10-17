# Sales Report Generator - 설치 및 실행 가이드

## 📋 사전 요구사항

시스템에 다음 소프트웨어가 설치되어 있어야 합니다:

- **Node.js** (v14 이상)
- **Python** (v3.8 이상)
- **pip** (Python 패키지 관리자)
- **OpenAI API Key** (GPT 분석 기능 사용 시)

## 🚀 설치 방법

### 1. 프로젝트 클론 또는 다운로드

```bash
cd /Users/junsangdong/Desktop/vibe-1122-acorn-ml-prediction
```

### 2. Python 패키지 설치

```bash
pip install -r requirements.txt
```

또는 Python3를 사용하는 경우:

```bash
pip3 install -r requirements.txt
```

### 3. Node.js 패키지 설치

```bash
npm install
```

### 4. 환경 변수 설정

`.env` 파일을 프로젝트 루트에 생성합니다:

```bash
touch .env
```

`.env` 파일에 다음 내용을 추가합니다:

```
OPENAI_API_KEY=your_openai_api_key_here
PORT=3000
```

**OpenAI API 키 발급 방법:**
1. https://platform.openai.com 방문
2. 로그인 또는 회원가입
3. API Keys 메뉴에서 새 키 생성
4. 생성된 키를 `.env` 파일에 붙여넣기

> ⚠️ **주의**: OpenAI API 키 없이도 기본 통계 분석과 차트는 생성되지만, GPT 기반 자연어 분석은 생성되지 않습니다.

## ▶️ 실행 방법

### 개발 모드 (자동 재시작)

```bash
npm run dev
```

### 프로덕션 모드

```bash
npm start
```

서버가 실행되면 다음과 같은 메시지가 표시됩니다:

```
==============================================
🚀 Sales Report Generator Server is running
==============================================
📍 URL: http://localhost:3000
📊 API Health: http://localhost:3000/api/health
==============================================
```

### 브라우저에서 접속

웹 브라우저를 열고 다음 URL로 접속합니다:

```
http://localhost:3000
```

## 📝 사용 방법

### 1. 파일 준비

분석할 CSV 또는 XLSX 파일을 준비합니다. 파일에는 다음 컬럼이 포함되어야 합니다:

- `Sales` (필수) - 매출 금액
- `Profit` (필수) - 이익 금액
- `Category` (권장) - 상품 카테고리
- `State` 또는 `Region` (권장) - 지역 정보
- `Sub-Category` (선택) - 세부 카테고리
- `Segment` (선택) - 고객 세그먼트
- `Order Date` 또는 `Date` (선택) - 주문 날짜

**예시 파일**: `Sample-100-Superstore.csv` 파일을 참고하세요.

### 2. 파일 업로드

웹 페이지에서 다음 두 가지 방법으로 파일을 업로드할 수 있습니다:

- **드래그 앤 드롭**: 파일을 브라우저 창으로 드래그
- **파일 선택**: "파일 선택" 버튼을 클릭하여 파일 선택

### 3. 리포트 생성

"리포트 생성" 버튼을 클릭합니다. 다음 단계가 자동으로 진행됩니다:

1. ✅ 파일 업로드
2. ✅ Pandas로 데이터 분석
3. ✅ GPT API로 분석 보고서 생성
4. ✅ Matplotlib 차트 생성
5. ✅ ReportLab으로 PDF 생성
6. ✅ PDF 다운로드

### 4. PDF 보고서 확인

생성된 PDF 파일이 자동으로 다운로드됩니다. PDF에는 다음 내용이 포함됩니다:

- **Executive Summary**: 주요 통계 요약
- **Category Performance**: 카테고리별 성과
- **Data Visualizations**: 6가지 차트
  - 카테고리별 매출
  - 지역별 이익 (상위 10개)
  - 서브카테고리별 매출 (상위 10개)
  - 세그먼트별 비교
  - 매출과 이익의 상관관계
  - 월별 매출 추세
- **AI-Generated Analysis**: GPT 기반 마케팅 전략 및 인사이트

## 🔧 문제 해결

### Python 패키지 설치 오류

```bash
# pip 업그레이드
pip install --upgrade pip

# 개별 패키지 재설치
pip install pandas matplotlib reportlab openai
```

### Node.js 패키지 설치 오류

```bash
# npm 캐시 정리
npm cache clean --force

# node_modules 삭제 후 재설치
rm -rf node_modules
npm install
```

### OpenAI API 오류

- `.env` 파일에 올바른 API 키가 설정되어 있는지 확인
- OpenAI 계정에 충분한 크레딧이 있는지 확인
- API 키 없이도 기본 통계와 차트는 생성됩니다

### 포트 변경

`.env` 파일에서 `PORT` 값을 변경합니다:

```
PORT=8080
```

### Python 버전 확인

```bash
python3 --version
```

Python 3.8 이상이 필요합니다.

### 차트 한글 폰트 문제 (Mac)

Mac에서는 기본적으로 AppleGothic 폰트를 사용합니다. 만약 한글이 제대로 표시되지 않으면 `analyze_sales.py` 파일에서 폰트를 변경할 수 있습니다:

```python
# analyze_sales.py 파일 상단
plt.rcParams['font.family'] = 'AppleGothic'  # Mac
# 또는
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
```

## 📊 생성되는 통계 항목

### 전체 통계
- 총 매출 (Total Sales)
- 총 이익 (Total Profit)
- 이익률 (Profit Margin)
- 평균 매출 (Average Sales)
- 평균 이익 (Average Profit)
- 총 주문 수 (Total Orders)
- 총 판매 수량 (Total Quantity)

### 카테고리별 분석
- 카테고리별 총 매출 및 이익
- 카테고리별 평균 매출
- 카테고리별 주문 수

### 지역별 분석
- 상위 10개 지역의 매출 및 이익
- 지역별 수익성 분석

### 세그먼트별 분석
- 고객 세그먼트별 매출 및 이익
- 세그먼트별 평균 매출

### 시계열 분석
- 월별 매출 추세
- 연도별 성장률

## 🔐 보안 권장사항

1. `.env` 파일을 절대 Git에 커밋하지 마세요
2. OpenAI API 키는 안전하게 보관하세요
3. 프로덕션 환경에서는 HTTPS를 사용하세요
4. 업로드 파일 크기 제한을 적절히 설정하세요 (현재 10MB)

## 📚 추가 리소스

- [Pandas 문서](https://pandas.pydata.org/docs/)
- [Matplotlib 문서](https://matplotlib.org/stable/contents.html)
- [ReportLab 문서](https://docs.reportlab.com/)
- [OpenAI API 문서](https://platform.openai.com/docs/)
- [Express.js 문서](https://expressjs.com/)

## 💡 팁

1. **대용량 파일**: 10MB 이상의 파일은 서버 설정에서 제한을 늘려야 합니다
2. **커스터마이징**: Python 스크립트를 수정하여 원하는 통계나 차트를 추가할 수 있습니다
3. **배치 처리**: 여러 파일을 순차적으로 처리할 수 있습니다
4. **스케줄링**: cron job을 사용하여 정기적으로 보고서를 생성할 수 있습니다

## 🐛 버그 리포트

문제가 발생하면 다음 정보를 포함하여 리포트해주세요:

1. 에러 메시지
2. 사용 중인 OS 및 버전
3. Python 버전
4. Node.js 버전
5. 업로드한 파일의 형식 및 크기

즐거운 데이터 분석 되세요! 🎉

