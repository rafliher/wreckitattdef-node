FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y nano

WORKDIR /opt
COPY ./src .
COPY .env /opt/.env

RUN pip install --no-cache-dir -r requirements.txt

ARG FLAG
RUN echo $FLAG > flag && chmod 444 flag

COPY ./main.sh /main.sh

RUN chmod +x /main.sh

CMD ["/main.sh"]