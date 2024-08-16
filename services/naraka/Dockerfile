FROM python:3.9-slim

ARG PASSWORD

WORKDIR /app

RUN apt-get update && \
    apt-get install -y nano openssh-server \
    gcc curl 

# Create ctfuser and set password
RUN useradd -m -d /app ctfuser && echo ctfuser:${PASSWORD} | chpasswd

# Configure SSH for ctfuser
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config && \
    echo "AllowUsers ctfuser" >> /etc/ssh/sshd_config

# Start SSH service
RUN ssh-keygen -A
RUN mkdir -p /run/sshd && chmod 755 /run/sshd

RUN apt update
RUN apt install python3-pip -y
RUN pip3 install flask==3.0.2 --break-system-packages

COPY /src .
COPY flag.txt ../

# Restrict ctfuser access to only the working directory
RUN chown -R ctfuser:ctfuser /app/scripts && \
    chmod 700 /app/scripts

# Restrict ctfuser access to only the working directory
RUN chown -R ctfuser:ctfuser /app/satanize.py && \
chmod 700 /app/satanize.py

COPY start.sh .
RUN chmod +x start.sh

# Start SSH service as root and then switch to ctfuser
CMD service ssh start && ./start.sh