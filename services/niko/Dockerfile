FROM public.ecr.aws/docker/library/python:slim

ARG PASSWORD

WORKDIR /opt

RUN apt-get update && \
    apt-get install -y nano openssh-server \
    gcc curl 

# Create ctfuser and set password
RUN useradd -m -d /opt ctfuser && echo ctfuser:${PASSWORD} | chpasswd

COPY src/ .

# Generate a random flag and write it to /opt/flag
RUN python3 -c "import random; import string; flag = ''.join(random.choices(string.digits, k=8)); open('/opt/flag', 'w').write(flag)"

# Change ownership of /opt and its contents to ctfuser
RUN chown -R ctfuser:ctfuser /opt

# Set restrictive permissions for the /opt directory and its contents
RUN chmod 700 /opt && \
    find /opt -type f -exec chmod 400 {} \;

# Allow write permissions only for /opt/server.py for ctfuser
RUN chmod 700 /opt/server.py

# Configure SSH for ctfuser
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config && \
    echo "AllowUsers ctfuser" >> /etc/ssh/sshd_config

# Start SSH service
RUN ssh-keygen -A
RUN mkdir -p /run/sshd && chmod 755 /run/sshd

RUN touch /flag.txt

RUN pip install -r requirements.txt
RUN chmod +x ./start.sh
RUN chmod +x ./niko

CMD service ssh start && ./start.sh

EXPOSE 8000
EXPOSE 22