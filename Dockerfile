FROM python:3.11-alpine AS code_and_dependencies

WORKDIR /usr/src/app
COPY ./dogofthehour.py .
COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM code_and_dependencies
ENV DOGNAMES=Sniff,Juci,Eddie,Cosmo
ENV CSV_OUT=/csv/doth.csv

CMD ["python", "dogofthehour.py"]
