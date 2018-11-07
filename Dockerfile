FROM python:2.7.15

ENV LANG C.UTF-8

RUN mkdir /kirk
WORKDIR /kirk
ADD requirements.txt /kirk/
RUN pip install -r requirements.txt
ADD ./src/backend/app_kirk_rest /kirk/

RUN python manage.py migrate
RUN python manage.py collectstatic

ENTRYPOINT ["python", "/kirk/manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
