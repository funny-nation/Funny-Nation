FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

RUN yoyo apply ./migrations

CMD ["python3", "main.py"]