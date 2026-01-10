FROM python:3.13-alpine
WORKDIR /app
COPY core/ ./core
CMD ["python", "core/main.py"]