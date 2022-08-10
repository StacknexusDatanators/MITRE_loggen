FROM python:3.8.8

COPY ./loggen /loggen
COPY ./logapi /logapi

COPY logcron /etc/cron.d/logcron


WORKDIR /loggen

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -y install cron

RUN chmod 0644 /etc/cron.d/logcron

RUN crontab /etc/cron.d/logcron

RUN touch /var/log/loggen.log

CMD cron &

WORKDIR /logapi

CMD ["uvicorn", "mainapi:app", "--host", "0.0.0.0", "--port", "8000"]