FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/LikeApp

COPY ./requirements.txt /usr/src/LikeApp/requirements.txt
RUN pip install -r /usr/src/LikeApp/requirements.txt

COPY . .

EXPOSE 8000