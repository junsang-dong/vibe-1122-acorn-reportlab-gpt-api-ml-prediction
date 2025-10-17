# 사용 가이드 (Usage Guide)

## 🎯 빠른 시작

### 방법 1: 자동 시작 스크립트 (권장)

```bash
./start.sh
```

이 스크립트는 자동으로:
- ✅ Node.js와 Python 설치 확인
- ✅ 패키지 설치
- ✅ 필요한 디렉토리 생성
- ✅ 서버 시작

### 방법 2: 수동 실행

```bash
# 1. 패키지 설치
npm install
pip3 install -r requirements.txt

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 OpenAI API 키 추가

# 3. 서버 시작
npm start
```

## 📊 분석 테스트

샘플 데이터로 분석 기능을 테스트:

```bash
python3 test_analysis.py
```

또는

```bash
npm test
```

## 🌐 웹 인터페이스 사용

### 1. 브라우저 접속

```
http://localhost:3000
```

### 2. 파일 업로드

**방법 A: 드래그 앤 드롭**
- CSV 또는 XLSX 파일을 업로드 박스로 드래그

**방법 B: 파일 선택**
- "파일 선택" 버튼 클릭
- 파일 선택 대화상자에서 파일 선택

### 3. 리포트 생성

- "리포트 생성 🚀" 버튼 클릭
- 진행 상황을 실시간으로 확인
- 완료되면 PDF가 자동으로 다운로드됨

## 📁 데이터 파일 형식

### 필수 컬럼

| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| `Sales` | 매출 금액 | 261.96 |
| `Profit` | 이익 금액 | 41.9136 |

### 권장 컬럼

| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| `Category` | 상품 카테고리 | Furniture, Office Supplies |
| `Sub-Category` | 세부 카테고리 | Bookcases, Chairs |
| `State` 또는 `Region` | 지역 정보 | California, West |
| `Segment` | 고객 세그먼트 | Consumer, Corporate |
| `Order Date` | 주문 날짜 | 11/8/2016 |
| `Quantity` | 판매 수량 | 2 |

### 예시 CSV 파일 구조

```csv
Row ID,Order ID,Order Date,Ship Date,Ship Mode,Customer ID,Customer Name,Segment,Country,City,State,Postal Code,Region,Product ID,Category,Sub-Category,Product Name,Sales,Quantity,Discount,Profit
1,CA-2016-152156,11/8/2016,11/11/2016,Second Class,CG-12520,Claire Gute,Consumer,United States,Henderson,Kentucky,42420,South,FUR-BO-10001798,Furniture,Bookcases,Bush Somerset Collection Bookcase,261.96,2,0,41.9136
```

## 📄 생성되는 PDF 보고서 내용

### 1. 표지 페이지
- 보고서 제목
- 생성 날짜

### 2. Executive Summary (요약)
- 총 매출
- 총 이익
- 이익률
- 총 주문 수
- 평균 매출
- 평균 이익

### 3. Category Performance (카테고리 성과)
- 카테고리별 총 매출
- 카테고리별 총 이익
- 주문 수
- 평균 매출

### 4. Data Visualizations (데이터 시각화)

#### 차트 1: 카테고리별 매출
- 가로 막대 차트
- 각 카테고리의 총 매출 비교

#### 차트 2: 상위 10개 지역별 이익
- 가로 막대 차트
- 양수(녹색), 음수(빨간색) 구분

#### 차트 3: 상위 10개 서브카테고리 매출
- 세로 막대 차트
- 가장 많이 팔린 세부 카테고리

#### 차트 4: 세그먼트별 비교
- 그룹 막대 차트
- 고객 세그먼트별 매출 및 이익

#### 차트 5: 매출-이익 상관관계
- 산점도
- 양수 이익(녹색), 음수 이익(빨간색)

#### 차트 6: 월별 매출 추세
- 선 그래프
- 시간에 따른 매출 변화

### 5. AI-Generated Analysis (AI 분석)

GPT API를 통해 생성되는 자연어 보고서:

- **전체 개요 (Executive Summary)**
  - 주요 수치 요약
  - 전반적인 비즈니스 상태

- **주요 발견 사항 (Key Findings)**
  - 데이터에서 발견된 중요한 인사이트
  - 주목할 만한 트렌드

- **카테고리 분석**
  - 각 카테고리의 성과 평가
  - 강점과 약점 분석

- **지역 분석**
  - 지역별 성과 비교
  - 수익성 높은 지역 식별

- **세그먼트 분석**
  - 고객 세그먼트별 특성
  - 타겟팅 전략 제안

- **개선 제안 및 마케팅 전략**
  - 구체적인 실행 계획
  - 우선순위 제안

- **결론**
  - 종합 요약
  - 다음 단계 제안

## 🎨 커스터마이징

### 차트 스타일 변경

`analyze_sales.py` 파일에서 차트 스타일을 수정할 수 있습니다:

```python
# 차트 색상 변경
plt.figure(figsize=(10, 6))
category_sales.plot(kind='barh', color='steelblue')  # 여기서 색상 변경
```

### GPT 프롬프트 수정

`generate_gpt_report.py` 파일에서 GPT 분석 내용을 수정할 수 있습니다:

```python
prompt = f"""당신은 전문 비즈니스 분석가입니다. 
다음 판매 데이터 통계를 분석하고, 한국어로 상세한 마케팅 전략 보고서를 작성해주세요.

보고서는 다음 구조를 따라야 합니다:
1. 전체 개요 (Executive Summary)
2. 주요 발견 사항 (Key Findings)
...
"""
```

### PDF 레이아웃 수정

`generate_pdf.py` 파일에서 PDF 디자인을 변경할 수 있습니다:

```python
# 제목 스타일
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,  # 폰트 크기
    textColor=colors.HexColor('#1f4788'),  # 색상
    spaceAfter=30,
    alignment=TA_CENTER,
)
```

## 🔍 트러블슈팅

### 문제: 서버가 시작되지 않음

**해결책:**
```bash
# 포트가 이미 사용 중인지 확인
lsof -ti:3000

# 프로세스 종료
kill -9 $(lsof -ti:3000)

# 또는 .env에서 포트 변경
PORT=8080
```

### 문제: Python 패키지 import 오류

**해결책:**
```bash
# Python 경로 확인
which python3

# 패키지 재설치
pip3 install --upgrade -r requirements.txt

# 가상환경 사용 (권장)
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 문제: GPT 분석이 생성되지 않음

**해결책:**
1. `.env` 파일의 `OPENAI_API_KEY` 확인
2. OpenAI 계정 크레딧 확인
3. 서버 로그에서 에러 메시지 확인

```bash
# 서버 로그 확인
npm start
```

### 문제: 차트에 한글이 깨짐

**해결책:**

`analyze_sales.py` 파일 수정:

**Mac:**
```python
plt.rcParams['font.family'] = 'AppleGothic'
```

**Windows:**
```python
plt.rcParams['font.family'] = 'Malgun Gothic'
```

**Linux:**
```python
plt.rcParams['font.family'] = 'NanumGothic'
```

### 문제: 파일 업로드 실패

**해결책:**
1. 파일 크기 확인 (10MB 이하)
2. 파일 형식 확인 (.csv, .xlsx, .xls)
3. 필수 컬럼 확인 (Sales, Profit)

## 💡 고급 사용법

### API 직접 호출

```bash
curl -X POST http://localhost:3000/api/generate-report \
  -F "file=@Sample-100-Superstore.csv" \
  --output report.pdf
```

### Python 스크립트 단독 실행

```bash
# 1. 데이터 분석만 실행
python3 analyze_sales.py Sample-100-Superstore.csv

# 2. GPT 분석 생성
python3 generate_gpt_report.py '{"total_sales": 123456, ...}'

# 3. PDF 생성
python3 generate_pdf.py '{"total_sales": 123456}' "분석 텍스트" '[]' output.pdf
```

### 배치 처리

여러 파일을 순차적으로 처리하는 스크립트:

```bash
#!/bin/bash
for file in data/*.csv; do
    echo "Processing $file..."
    curl -X POST http://localhost:3000/api/generate-report \
      -F "file=@$file" \
      --output "reports/$(basename $file .csv).pdf"
done
```

## 📈 성능 최적화

### 대용량 파일 처리

`server.js`에서 파일 크기 제한 조정:

```javascript
const upload = multer({
    storage: storage,
    limits: {
        fileSize: 50 * 1024 * 1024 // 50MB로 증가
    }
});
```

### 동시 요청 처리

동시에 여러 사용자가 사용하는 경우:

```bash
# PM2로 프로세스 관리
npm install -g pm2
pm2 start server.js -i max  # CPU 코어 수만큼 인스턴스 생성
```

## 🔗 통합 및 확장

### REST API로 통합

다른 애플리케이션에서 API 호출:

```javascript
// JavaScript 예시
const formData = new FormData();
formData.append('file', fileBlob, 'data.csv');

fetch('http://localhost:3000/api/generate-report', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'report.pdf';
    a.click();
});
```

### 데이터베이스 통합

데이터베이스에서 직접 데이터 가져오기:

```python
import pandas as pd
import psycopg2

# PostgreSQL 연결
conn = psycopg2.connect("dbname=sales user=postgres")
df = pd.read_sql_query("SELECT * FROM sales_data", conn)

# 분석 실행
result = analyze_sales_data(df)
```

## 📞 지원

문제가 있거나 질문이 있으시면:

1. `SETUP_GUIDE.md` 참조
2. 서버 로그 확인
3. GitHub Issues 생성 (프로젝트 저장소)

즐거운 분석 되세요! 🎉

