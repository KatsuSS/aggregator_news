FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip
WORKDIR /home/aggregator
COPY app app
COPY migrations migrations
COPY aggregator.py config.py boot.sh ./
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN pip install -r requirements.txt
RUN chmod +x boot.sh
ENV FLASK_APP aggregator.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
