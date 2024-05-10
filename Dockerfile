FROM python:3.8

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py collectstatic

RUN python manage.py makemigrations
RUN python manage.py migrate