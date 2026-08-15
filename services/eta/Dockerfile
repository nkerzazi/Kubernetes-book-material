# Image volontairement lourde : c'est le contre-exemple du chapitre 2 et le
# sujet du chapitre 9 (demarrage lent, empreinte memoire, autoscaling).
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY escale_eta ./escale_eta
COPY escale_common ./escale_common
ENV PYTHONUNBUFFERED=1 INFERENCE_MODE=mock STARTUP_DELAY_S=30
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "escale_eta.main:app", "--host", "0.0.0.0", "--port", "8000"]
