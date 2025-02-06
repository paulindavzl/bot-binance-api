# Use uma imagem base com Python
FROM python:3.12.8-slim

# Instala dependências necessárias
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH" && \
    poetry --version
ENV PATH="/root/.local/bin:$PATH"

# Define o diretório de trabalho como /app
WORKDIR /app

# Copia os arquivos de configuração do Poetry para o contêiner
COPY pyproject.toml poetry.lock* README.md init_app.py init_configure.py init_tests.py /app/

# Copia o restante do código para o contêiner
COPY src/ /app/src/
COPY tests/ /app/tests/

# Instala as dependências do projeto
RUN poetry install --no-interaction

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Defina o comando para iniciar a aplicação Flask
CMD ["poetry", "run", "app"]