FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY app.py test_app.py ./

EXPOSE 8000

CMD ["python", "app.py"]
