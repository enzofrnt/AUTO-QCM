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

ENV env=dev

COPY ./requirements.dev.txt .

RUN pip install --no-cache-dir -r requirements.dev.txt

RUN rm ./requirements.dev.txt

CMD python manage.py wait_for_db \
    && python manage.py makemigrations \
    && python manage.py migrate --noinput \
    && python manage.py runserver 0.0.0.0:8000


FROM base AS prod

ENV env=prod

COPY ./requirements.prod.txt .

RUN pip install --no-cache-dir -r requirements.prod.txt

RUN rm ./requirements.prod.txt

RUN mkdir -p /app/log
RUN touch /app/log/log.txt

# Pour sécuriser la prod on va retirer la command qui permet de remplir la base de données avec des données factices car
# cela peut être dangereux en prod
RUN rm -rf ./app/management/commands/fill_fake_data.py

RUN python manage.py collectstatic --noinput

CMD python manage.py wait_for_db \
    && python manage.py migrate --noinput \
    && gunicorn auto_qcm.wsgi --bind 0.0.0.0:8000
