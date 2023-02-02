FROM python:3.11-alpine

WORKDIR /usr/src/app
COPY ./dogofthehour.py .
COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV DOGNAMES=Sniff,Juci,Eddie,Cosmo
ENV CSV_OUT=/csv/doth.csv

CMD ["python", "dogofthehour.py"]
