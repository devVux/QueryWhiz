
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
COPY nginx.conf /etc/nginx/nginx.conf

#RUN pip install -r requirements.txt

COPY app/ ./app/

EXPOSE 5000

CMD ["python", "-m", "app.main"]

