FROM python:3.10-slim AS base

# Installer les dépendances nécessaires pour AMC et PostgreSQL
RUN apt-get update && \
    apt-get install -y \
    auto-multiple-choice && \
    apt-get install -y gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN rm ./requirements.txt

COPY ./auto_qcm .

FROM base AS dev

CMD python manage.py wait_for_db \
    && python manage.py makemigrations \
    && python manage.py migrate --noinput \
    && python manage.py runserver 0.0.0.0:8000


FROM base AS prod

COPY ./requirements.pro.txt .

RUN pip install --no-cache-dir -r requirements.prod.txt

RUN rm ./requirements.pro.txt

CMD [ "gunicorn", "auto_qcm.wsgi:application", "--bind", "0.0.0.0:8000" ]  # Correction de la commande gunicorn