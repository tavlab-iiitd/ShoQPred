FROM python:3.7

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY manage.py gunicorn-cfg.py .env ./
COPY app app
COPY authentication authentication
COPY core core
COPY weights weights
COPY staticfiles staticfiles

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 5005

ENV DEBUG True

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]