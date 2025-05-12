FROM python:3.10-bookworm

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Atualiza pacotes e instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libffi-dev \
    build-essential \
    curl \
    bash \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

# Define o diretório de trabalho
WORKDIR /app

# Copia arquivos de dependência primeiro para cache eficiente
COPY pyproject.toml poetry.lock ./

# Instala as dependências Python
RUN poetry install --no-root

# Copia o restante do código
COPY . .

# Expõe a porta padrão do Django
EXPOSE 8000

RUN chmod +x ./init.sh

