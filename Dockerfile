FROM python:3.6-alpine

ENV LANG C.UTF-8

RUN mkdir /kirk
WORKDIR /kirk
ADD requirements.txt /kirk/
RUN pip install -r requirements.txt
ADD ./src/backend/app_kirk_rest /kirk/

RUN python3 manage.py migrate
RUN python3 manage.py collectstatic

ENTRYPOINT ["python3", "/kirk/manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
