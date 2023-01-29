FROM selenium/standalone-firefox

ENV PYTHONUNBUFFERED=1 \
    GUNICORN_WORKERS=2

RUN sudo apt-get update
RUN sudo apt install --assume-yes python3-pip
RUN sudo apt install python-is-python3
RUN sudo apt install --assume-yes gunicorn


COPY ./requirements.txt ./

RUN pip3 install -r ./requirements.txt

COPY ./kapsarc_data_scraper ./kapsarc_data_scraper \
     ./app.py ./ \
     ./services.py ./

EXPOSE 5050

WORKDIR /

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:5050 -w $GUNICORN_WORKERS app"]

HEALTHCHECK CMD curl --fail http://localhost:5050/version || exit 1

