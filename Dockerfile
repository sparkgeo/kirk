FROM python:3.8-alpine

ENV LANG C.UTF-8

WORKDIR /kirk
ADD ./src/backend/app_kirk_rest /kirk/
ADD requirements.txt /kirk/
RUN ls /kirk

# apk update
RUN apk add --no-cache curl py3-psycopg2
RUN apk add --virtual build-dependencies --no-cache python3 pkgconfig python3-dev openssl-dev libffi-dev musl-dev make gcc py3-psycopg2 \
    && pip install -r /kirk/requirements.txt \
    && apk del build-dependencies

ENV PYTHONPATH='/usr/lib/python3.8:/usr/lib/python3.8/site-packages'

RUN python manage.py migrate \
  && python manage.py collectstatic

ENTRYPOINT ["python", "/kirk/manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
