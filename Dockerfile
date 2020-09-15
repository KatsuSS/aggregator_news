FROM python:3.7-alpine

RUN adduser -D aggregator

WORKDIR /home/aggregator

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY aggregator.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP aggregator.py

RUN chown -R aggregator:aggregator ./
USER aggregator

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]