FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirror.abrha.net/repository/pypi/simple

RUN adduser --disabled-password --gecos "" appuser

RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app/staticfiles /app/media

COPY . .
RUN chown -R appuser:appuser /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown appuser:appuser /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

USER appuser

EXPOSE 8000