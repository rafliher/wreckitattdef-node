FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y nano

WORKDIR /opt
COPY ./src .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./flag.txt /opt/flag.txt

COPY ./main.sh /main.sh

RUN chmod +x /main.sh

CMD ["/main.sh"]