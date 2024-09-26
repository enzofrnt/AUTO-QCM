FROM python:3.10-slim AS base

RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN rm ./requirements.txt

COPY ./auto_qcm .

FROM base AS dev

COPY ./requirements.dev.txt .

RUN pip install --no-cache-dir -r requirements.dev.txt

RUN rm ./requirements.dev.txt

CMD python manage.py wait_for_db \
    && python manage.py makemigrations \
    && python manage.py migrate --noinput \
    && python manage.py runserver 0.0.0.0:8000


FROM base AS prod

COPY ./requirements.prod.txt .

RUN pip install --no-cache-dir -r requirements.prod.txt

RUN rm ./requirements.prod.txt

CMD [ "gunicorn", "auto_qcm.wsgi:application", "--bind", "0.0.0.0:8000" ]