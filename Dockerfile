FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["sh", "-c", "echo 'Container Started' > /app/container_started_log.txt && python app.py &> /app/app_logs.txt"]
