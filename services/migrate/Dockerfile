FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY escale_migrate ./escale_migrate
COPY escale_common ./escale_common
COPY migrations ./migrations
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "escale_migrate.main"]
