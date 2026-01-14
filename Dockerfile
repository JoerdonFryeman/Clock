FROM python:3.13-alpine
RUN pip install psutil
WORKDIR /app
COPY main.py .
COPY core/ ./core
COPY config_files/ ./config_files
CMD ["python", "main.py"]