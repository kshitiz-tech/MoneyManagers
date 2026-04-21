FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    KIVY_NO_ARGS=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    fluxbox \
    libffi-dev \
    libgl1-mesa-glx \
    libgles2-mesa \
    libglib2.0-0 \
    libgstreamer1.0-0 \
    libjpeg62-turbo \
    libmtdev1 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libzbar0 \
    novnc \
    pkg-config \
    websockify \
    x11vnc \
    xvfb \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh && mkdir -p /app/data

EXPOSE 6080

CMD ["./start.sh"]
