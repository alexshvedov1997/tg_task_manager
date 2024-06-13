FROM python:3.10.6

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt


COPY . /app/

ADD start.sh /
RUN chmod +x /start.sh
