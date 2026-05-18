# بیلد با Dockerfile جدید (کاملاً آفلاین)
# docker build --network=none -f Dockerfile.offline -t todo_app-backend:offline .

# Dockerfile جدید
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# کپی پکیج‌های نصب شده از venv به Docker
COPY site-packages/ /usr/local/lib/python3.12/site-packages/
COPY site-packages/ /root/.cache/pip/

# کپی requirements.txt
COPY requirements.txt .

# نصب بدون اینترنت (فقط از cache استفاده کن)
RUN pip install --no-index --ignore-installed --find-links=/root/.cache/pip -r requirements.txt || \
    pip install --no-deps --ignore-installed --find-links=/usr/local/lib/python3.12/site-packages -r requirements.txt

RUN adduser --disabled-password --gecos "" appuser

COPY . .
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]