FROM python:3.8-slim-buster

COPY docker_requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py
COPY static/test.html /app/static/test.html
COPY misc/imagenet_class_index.json /app/misc/imagenet_class_index.json
WORKDIR /app

# Expose is NOT supported by Heroku
# EXPOSE 5000

RUN groupadd -r myuser && useradd -r -g myuser myuser
RUN chown -R myuser. /app

USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn --log-level=debug --bind 0.0.0.0:$PORT -k gevent app:app
