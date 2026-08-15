FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY escale_worker ./escale_worker
COPY escale_api ./escale_api
COPY escale_common ./escale_common
ENV PYTHONUNBUFFERED=1
EXPOSE 9100
CMD ["python", "-m", "escale_worker.main"]
