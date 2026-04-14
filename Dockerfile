FROM python:3.12-slim

# No extra packages needed — stdlib only
WORKDIR /app

COPY app.py .

# Ensure Python output is not buffered so logs appear in docker logs immediately
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
