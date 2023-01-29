FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1 \
    GUNICORN_WORKERS=2


COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY ./kapsarc_data_scraper ./kapsarc_data_scraper \
     ./app.py ./ \
     ./services.py ./

EXPOSE 5050

WORKDIR /

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:5050 -w $GUNICORN_WORKERS app"]

HEALTHCHECK CMD curl --fail http://localhost:5050/version || exit 1

