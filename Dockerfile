FROM python:3.8.8

COPY ./loggen /loggen
COPY ./logapi /logapi



WORKDIR /loggen

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -y install cron

COPY logcron /etc/cron.d/logcron


RUN chmod 0644 /etc/cron.d/logcron

RUN crontab /etc/cron.d/logcron

RUN touch /var/log/loggen.log

CMD cron && tail -f /var/log/loggen.log
CMD service cron start

WORKDIR /logapi

CMD cron


CMD ["uvicorn", "mainapi:app", "--host", "0.0.0.0", "--port", "8000"]

