FROM python:3.14-slim

WORKDIR /app

# Instala o Poetry
RUN pip install --no-cache-dir poetry

# Configura o Poetry para instalar no ambiente global do container
RUN poetry config virtualenvs.create false

# Copia os arquivos de dependências
COPY pyproject.toml poetry.lock ./

# Instala as dependências
RUN poetry install --only main --no-root --no-interaction

# Copia o restante do projeto
COPY . .

# Disponibiliza a porta do Streamlit
EXPOSE 8501

# Inicializa o chatbot
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]