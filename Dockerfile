FROM python:3.6-alpine as alpinebase
FROM alpinebase as alpinebuilder
ENV LANG C.UTF-8

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt
RUN apk add --no-cache curl python3 pkgconfig python3-dev openssl-dev libffi-dev musl-dev make gcc  py3-psycopg2
RUN pip install --install-option="--prefix=/install" -r /requirements.txt


FROM alpinebase
WORKDIR /kirk
COPY --from=alpinebuilder /install /usr/local
ADD ./src/backend/app_kirk_rest /kirk/

RUN python manage.py migrate
RUN python manage.py collectstatic

ENTRYPOINT ["python", "/kirk/manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
