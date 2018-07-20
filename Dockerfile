FROM python:2.7.15

ENV LANG C.UTF-8

RUN mkdir /kirk
WORKDIR /kirk
ADD requirements.txt /kirk/
RUN pip install -r requirements.txt
ADD ./src/backend/app_kirk_rest /kirk/

ENTRYPOINT ["python", "/kirk/manage.py", "runserver", "", "1.2.3.4:8000"]
