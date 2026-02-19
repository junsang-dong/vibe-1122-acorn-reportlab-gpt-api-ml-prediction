# Sales Report Generator - Railway 배포용
# Node.js + Python 하이브리드 앱

FROM node:20-slim

# Python 3 및 빌드 의존성 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Python을 python3로 심볼릭 링크 (spawn 'python3' 호환)
RUN ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /app

# Node.js 의존성 설치
COPY package*.json ./
RUN npm ci --omit=dev

# Python 의존성 설치
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . .

# Matplotlib 헤드리스 모드 (서버/컨테이너 환경)
ENV MPLBACKEND=Agg

# Railway가 할당하는 PORT 사용
EXPOSE 8080

CMD ["npm", "start"]
