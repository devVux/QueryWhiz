
FROM python:3.9-slim

WORKDIR /app

COPY .env ./
COPY requirements.txt ./

RUN apt-get update && apt-get install -y vim
RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./settings ./settings
COPY ./docs ./docs

EXPOSE 5000

CMD ["python", "-m", "app.main"]

