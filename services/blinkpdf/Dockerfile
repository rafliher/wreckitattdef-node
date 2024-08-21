FROM python:3.10-slim-buster

ARG PASSWORD

WORKDIR /opt

RUN apt-get update && \
    apt-get install -y nano openssh-server \
    gcc curl 

# Create ctfuser and set password
RUN useradd -m -d /opt ctfuser && echo ctfuser:${PASSWORD} | chpasswd

COPY src/ .

# Restrict ctfuser access to only the working directory
RUN chown -R ctfuser:ctfuser /opt && \
    chmod 700 /opt

# Configure SSH for ctfuser
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config && \
    echo "AllowUsers ctfuser" >> /etc/ssh/sshd_config

# Start SSH service
RUN ssh-keygen -A
RUN mkdir -p /run/sshd && chmod 755 /run/sshd

RUN touch /flag.txt

COPY ./flag.txt /flag.txt

COPY ./main.sh ./main.sh

RUN pip install -r requirements.txt
RUN chmod +x ./main.sh

CMD service ssh start && ./main.sh

# EXPOSE 5111
# EXPOSE 22
