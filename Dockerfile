
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./settings ./settings
COPY ./docs ./docs

EXPOSE 5000

CMD ["python", "-m", "app.main"]

