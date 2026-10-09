# Build from repo root: docker build --build-context frontend=app/frontend app/backend/
FROM public.ecr.aws/docker/library/python:3.12-slim

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:1.1.0 /lambda-adapter /opt/extensions/lambda-adapter

ENV PORT=8080
ENV AWS_LWA_READINESS_CHECK_PATH=/health
ENV FRONTEND_INDEX=/app/frontend/index.html

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py /app/main.py
COPY --from=frontend index.html /app/frontend/index.html

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
