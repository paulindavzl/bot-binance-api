# Use uma imagem base com Python
FROM python:3.13-slim

# Instale dependências necessárias
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instale o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - 
ENV PATH="/root/.local/bin:$PATH"

# Defina o diretório de trabalho como /src
WORKDIR /src

# Copie os arquivos de configuração do Poetry para o contêiner
COPY pyproject.toml poetry.lock* /src/

# Copie a pasta libs para dentro do diretório src
COPY libs /src/libs

# Instale as dependências do projeto
RUN poetry install --no-interaction --no-dev

# Copie o restante do código para o contêiner
COPY . /src/

# Exponha a porta usada pelo Flask (ajuste conforme necessário)
EXPOSE 5000

# Defina o comando para iniciar a aplicação Flask
CMD ["poetry", "run", "app"]
