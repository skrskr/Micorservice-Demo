FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN pip install -U pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

# # CMD python manage.py runserver 0.0.0.0:8000

# ENTRYPOINT [ "python manage.py runserver 0.0.0.0:8000" ]

