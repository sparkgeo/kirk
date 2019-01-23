FROM python:3.6-alpine as alpinebuilder
ENV LANG C.UTF-8

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt
RUN apk add --no-cache curl python3 pkgconfig python3-dev openssl-dev libffi-dev musl-dev make gcc
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM python:3.6-alpine as alpinebase
WORKDIR /kirk
COPY --from=alpinebuilder /install /usr/local
ADD ./src/backend/app_kirk_rest /kirk/
RUN apk add --no-cache py3-psycopg2

RUN python manage.py migrate
RUN python manage.py collectstatic

ENTRYPOINT ["python", "/kirk/manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
