FROM python:3.10.6

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

ENV FLASK_APP "backend/server"
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install bootstrap-flask
ADD ./src /code/
EXPOSE 5000

CMD flask --app server run --host=0.0.0.0
