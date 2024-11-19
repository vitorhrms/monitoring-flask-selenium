# Imagem base do Python 3.10
FROM python:3.10-slim

# Instalação de dependências do sistema operacional
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    unzip \
    libx11-dev \
    libx11-6 \
    libgbm-dev \
    libasound2 \
    libnss3 \
    libnspr4 \
    libxcomposite1 \
    libxrandr2 \
    libgtk-3-0 \
    libatk-bridge2.0-0 \
    libxss1 \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    --no-install-recommends

# Baixar e instalar o Chrome
RUN curl -sS https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt-get -y -f install && \
    rm google-chrome-stable_current_amd64.deb

# Instalar o ChromeDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget https://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# EXPOSE 3000

CMD ["python", "app.py"]