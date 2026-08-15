# Etape 5 — pip ne conserve pas son cache dans la couche.

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "escale_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
