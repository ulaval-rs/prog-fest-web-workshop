FROM python:3.10-buster

WORKDIR /app

COPY ./web_app /app/web_app
COPY ./app.py /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
