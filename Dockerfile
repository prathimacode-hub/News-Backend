FROM python:3.8.10-slim
RUN apt-get update && apt-get install -y build-essential libkrb5-dev

RUN mkdir /app
WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt
CMD ["gunicorn", "manage.py", "runserver"]