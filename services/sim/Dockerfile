FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY escale_sim ./escale_sim
COPY escale_common ./escale_common
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "escale_sim.main"]
