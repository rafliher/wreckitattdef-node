FROM python:3.10-slim-buster

RUN apt-get update
RUN apt-get install -y nano
RUN apt-get install -y pkg-config

WORKDIR /opt
COPY ./src .

RUN pip install --no-cache-dir -r requirements.txt

# RUN python -u ./app.py

# COPY ./flag.txt /flag.txt

# COPY ./main.sh /main.sh

# RUN chmod +x /main.sh

<<<<<<< HEAD
# CMD ["/main.sh"]
=======
CMD service ssh start && /main.sh
>>>>>>> bf2ec842703d4857cf6052d02a8d44aa70a5aa8d
