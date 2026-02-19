# Sales Report Generator - Railway 배포용
# Node.js + Python 하이브리드 앱

FROM node:20-slim

# Python 3 및 빌드 의존성 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Node.js 의존성 설치
COPY package*.json ./
RUN npm ci --omit=dev

# Python 가상환경 생성 및 의존성 설치 (PEP 668 대응)
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . .

# Matplotlib 헤드리스 모드 (서버/컨테이너 환경)
ENV MPLBACKEND=Agg

# Railway가 할당하는 PORT 사용
EXPOSE 8080

CMD ["npm", "start"]
