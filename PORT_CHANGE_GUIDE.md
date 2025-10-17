# 🔧 포트 변경 가이드

## ✅ 포트가 8080으로 변경되었습니다!

localhost:3000이 이미 사용 중이어서 기본 포트를 **8080**으로 변경했습니다.

---

## 🚀 빠른 시작

```bash
# 서버 시작
npm start

# 브라우저 접속
http://localhost:8080
```

---

## ⚙️ 포트 설정 확인

### 1. .env 파일 확인

```bash
cat .env
```

다음과 같이 표시되어야 합니다:
```
OPENAI_API_KEY=your_openai_api_key_here
PORT=8080
```

### 2. 수동으로 포트 변경하기

다른 포트를 사용하고 싶다면:

```bash
# .env 파일 수정
echo "PORT=9000" >> .env

# 또는 텍스트 에디터로 수정
nano .env
```

### 3. 일시적으로 다른 포트 사용

``bash
# 환경 변수로 직접 지정
PORT=9000 npm start
```

---

## 📝 변경된 파일 목록

다음 파일들이 포트 8080으로 업데이트되었습니다:

- ✅ `server.js` - 기본 포트를 8080으로 변경
- ✅ `.env` - PORT=8080 설정
- ✅ `start.sh` - 자동 생성 시 8080 사용
- ✅ `README.md` - 모든 예시를 8080으로 업데이트

---

## 🔍 포트 사용 확인

### 포트가 사용 중인지 확인

```bash
# Mac/Linux
lsof -i :8080

# 특정 포트 사용 프로세스 종료
kill -9 $(lsof -ti:8080)
```

### 사용 가능한 포트 찾기

일반적으로 사용 가능한 포트:
- 8080 (현재 설정)
- 8000
- 8888
- 9000
- 5000

---

## ✨ 자주 묻는 질문

### Q: 포트를 다시 3000으로 변경하려면?

```bash
echo "PORT=3000" > .env
npm start
```

### Q: 여러 포트에서 동시에 실행하려면?

```bash
# 터미널 1
PORT=8080 npm start

# 터미널 2
PORT=9000 npm start
```

### Q: 브라우저가 자동으로 열리지 않아요

```bash
# Mac
open http://localhost:8080

# Linux
xdg-open http://localhost:8080

# 또는 수동으로 브라우저를 열고 접속
```

---

## 🎉 준비 완료!

이제 다음 명령으로 시작하세요:

```bash
npm start
```

**새로운 주소: http://localhost:8080** 🚀

---

*문제가 계속되면 `SETUP_GUIDE.md`를 참고하세요.*

