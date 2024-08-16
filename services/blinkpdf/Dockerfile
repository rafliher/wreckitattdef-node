FROM python:3.10-slim-buster

ARG PASSWORD

RUN apt-get update && apt-get install -y nano

# Create ctfuser and set password
RUN useradd -m -d /app ctfuser && echo ctfuser:${PASSWORD} | chpasswd

# Configure SSH for ctfuser
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config && \
    echo "AllowUsers ctfuser" >> /etc/ssh/sshd_config

# Start SSH service
RUN ssh-keygen -A
RUN mkdir -p /run/sshd && chmod 755 /run/sshd

WORKDIR /opt
COPY ./src .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./flag.txt /flag.txt

COPY ./main.sh /main.sh

RUN chown -R ctfuser:ctfuser /opt && \
    chmod 700 /opt

RUN chmod +x /main.sh

CMD service ssh start && ./main.sh