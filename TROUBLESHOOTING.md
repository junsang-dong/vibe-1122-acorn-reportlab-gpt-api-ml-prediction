# 🔧 문제 해결 가이드 (Troubleshooting Guide)

## ✅ 해결된 문제: "보고서 생성 중 오류 발생"

### 🔍 문제 원인
**ReportLab 패키지가 설치되지 않았음**

### 🛠️ 해결 과정

#### 1. 문제 진단
```bash
# Python 패키지 확인
pip3 list | grep -E "(pandas|matplotlib|reportlab|openai)"

# 결과: reportlab이 누락됨
matplotlib                   3.7.2
openai                       1.107.1
pandas                       2.0.3
# reportlab 누락!
```

#### 2. 해결 방법
```bash
# 누락된 패키지 설치
pip3 install reportlab seaborn numpy pillow
```

#### 3. 테스트 및 확인
```bash
# 분석 스크립트 테스트
python3 test_analysis.py

# API 직접 테스트
curl -X POST http://localhost:8080/api/generate-report \
  -F "file=@Sample-100-Superstore.csv" \
  --output test-report.pdf

# PDF 생성 확인
file test-report.pdf
# 결과: PDF document, version 1.4, 9 pages
```

---

## 🚨 일반적인 오류 및 해결 방법

### 1. Python 패키지 관련 오류

#### 오류: `ModuleNotFoundError: No module named 'reportlab'`
**해결:**
```bash
pip3 install reportlab
```

#### 오류: `ModuleNotFoundError: No module named 'pandas'`
**해결:**
```bash
pip3 install pandas matplotlib seaborn numpy
```

#### 오류: `ModuleNotFoundError: No module named 'openai'`
**해결:**
```bash
pip3 install openai
```

### 2. 서버 관련 오류

#### 오류: `EADDRINUSE: address already in use :::8080`
**해결:**
```bash
# 포트 사용 중인 프로세스 확인
lsof -i :8080

# 프로세스 종료
kill -9 $(lsof -ti:8080)

# 또는 다른 포트 사용
PORT=9000 npm start
```

#### 오류: `Cannot GET /`
**해결:**
```bash
# 서버 상태 확인
curl http://localhost:8080/api/health

# 서버 재시작
npm start
```

### 3. 파일 업로드 관련 오류

#### 오류: `지원하지 않는 파일 형식입니다`
**해결:**
- CSV 또는 XLSX 파일만 업로드 가능
- 파일 확장자 확인 (.csv, .xlsx, .xls)

#### 오류: `파일 크기가 너무 큽니다`
**해결:**
- 현재 10MB 제한
- 더 큰 파일을 위해 `server.js`에서 제한 수정:
```javascript
limits: {
    fileSize: 50 * 1024 * 1024 // 50MB로 증가
}
```

### 4. 데이터 관련 오류

#### 오류: `필수 컬럼이 없습니다`
**해결:**
- CSV 파일에 `Sales`와 `Profit` 컬럼이 있는지 확인
- 컬럼명이 정확한지 확인 (대소문자 구분)

#### 오류: `데이터 분석 중 오류가 발생했습니다`
**해결:**
```bash
# 데이터 파일 직접 테스트
python3 test_analysis.py

# 에러 메시지 확인
python3 analyze_sales.py your_file.csv
```

### 5. GPT API 관련 오류

#### 오류: `OPENAI_API_KEY 환경 변수가 설정되지 않았습니다`
**해결:**
```bash
# .env 파일 생성/수정
echo "OPENAI_API_KEY=sk-..." > .env

# 또는 환경 변수로 직접 설정
export OPENAI_API_KEY=sk-...
```

#### 오류: `GPT 분석을 생성할 수 없습니다`
**해결:**
- API 키가 유효한지 확인
- OpenAI 계정에 충분한 크레딧이 있는지 확인
- 네트워크 연결 확인

> 💡 **참고**: GPT API 오류가 있어도 기본 통계와 차트는 생성됩니다.

---

## 🔍 디버깅 방법

### 1. 서버 로그 확인
```bash
# 서버를 포그라운드에서 실행하여 로그 확인
npm start

# 또는 개발 모드로 실행
npm run dev
```

### 2. Python 스크립트 개별 테스트
```bash
# 1단계: 데이터 분석 테스트
python3 analyze_sales.py Sample-100-Superstore.csv

# 2단계: GPT 분석 테스트 (API 키 필요)
python3 generate_gpt_report.py '{"total_sales": 1000}'

# 3단계: PDF 생성 테스트
python3 generate_pdf.py '{"total_sales": 1000}' "테스트 분석" '[]' test.pdf
```

### 3. 브라우저 개발자 도구 확인
1. F12 키로 개발자 도구 열기
2. Network 탭에서 API 요청 확인
3. Console 탭에서 JavaScript 오류 확인

### 4. 파일 권한 확인
```bash
# Python 스크립트 실행 권한 확인
ls -la *.py

# 필요시 실행 권한 부여
chmod +x *.py
```

---

## 🚀 성능 최적화

### 1. 대용량 파일 처리
```bash
# 메모리 사용량 모니터링
top -pid $(pgrep -f "node server.js")

# 필요시 Node.js 메모리 제한 증가
node --max-old-space-size=4096 server.js
```

### 2. 차트 생성 최적화
```python
# analyze_sales.py에서 차트 해상도 조정
plt.savefig(chart_path, dpi=150, bbox_inches='tight')  # 300에서 150으로 감소
```

### 3. PDF 생성 최적화
```python
# generate_pdf.py에서 이미지 크기 조정
img = Image(chart_path, width=4*inch, height=2.4*inch)  # 크기 감소
```

---

## 📞 추가 지원

### 로그 수집
문제가 지속되면 다음 정보를 수집해주세요:

```bash
# 시스템 정보
python3 --version
node --version
npm --version

# 설치된 패키지
pip3 list | grep -E "(pandas|matplotlib|reportlab|openai)"
npm list

# 서버 로그
npm start 2>&1 | tee server.log

# 에러 재현
python3 test_analysis.py
```

### 일반적인 해결 순서
1. ✅ Python 패키지 재설치
2. ✅ 서버 재시작
3. ✅ 브라우저 캐시 삭제
4. ✅ 파일 권한 확인
5. ✅ 로그 확인

---

## 🎉 성공 확인

다음 명령들이 모두 성공하면 정상 작동:

```bash
# 1. 서버 상태 확인
curl http://localhost:8080/api/health

# 2. 분석 테스트
python3 test_analysis.py

# 3. API 테스트
curl -X POST http://localhost:8080/api/generate-report \
  -F "file=@Sample-100-Superstore.csv" \
  --output test.pdf

# 4. PDF 확인
file test.pdf
```

**모든 테스트가 성공하면 웹에서 정상 작동합니다!** 🚀

---

*문제가 계속되면 이 가이드를 참고하거나 GitHub Issues에 문의해주세요.*
