FROM public.ecr.aws/docker/library/python:slim

ARG PASSWORD

WORKDIR /opt

RUN apt-get update && \
    apt-get install -y nano openssh-server \
    gcc curl 

# Create ctfuser and set password
RUN useradd -m -d /opt ctfuser && echo ctfuser:${PASSWORD} | chpasswd

# Restrict ctfuser access to only the working directory
RUN chown -R ctfuser:ctfuser /opt && \
    chmod 700 /opt

# Configure SSH for ctfuser
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config && \
    echo "AllowUsers ctfuser" >> /etc/ssh/sshd_config

# Start SSH service
RUN service ssh start

COPY src/ .
RUN touch /flag.txt

# Generate a random flag and write it to /opt/flag
RUN python3 -c "import random; import string; flag = ''.join(random.choices(string.ascii_letters + string.digits, k=8)); open('/opt/flag', 'w').write(flag)"

RUN pip install -r requirements.txt
RUN chmod +x ./start.sh

EXPOSE 8000
EXPOSE 22

USER ctfuser

CMD ./start.sh
