FROM ubuntu:latest
LABEL authors="eudis"
# Fase de build
FROM python:3.12.4 as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Fase final (imagem menor)
FROM python:3.12.4

WORKDIR /app

# Copia apenas as dependências instaladas da fase de build
COPY --from=builder /root/.local /root/.local
COPY . .

# Adiciona o diretório de instalação ao PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cria um usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "seu_app.wsgi:application"]
ENTRYPOINT ["top", "-b"]