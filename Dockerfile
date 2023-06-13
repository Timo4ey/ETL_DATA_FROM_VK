FROM python:3

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -qy gcc cron openssh-client flake8 locales vim

WORKDIR /service

COPY . .

RUN pip install poetry
RUN poetry install

CMD [ "make", "start"]