FROM public.ecr.aws/docker/library/python:slim

ARG PASSWORD

WORKDIR /opt

RUN apt-get update
RUN apt-get install -y nano openssh-server \
    gcc curl 

RUN echo root:${PASSWORD} | chpasswd
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN service ssh start

COPY src/ .
RUN touch /flag.txt

RUN python3 -c "import random; import string; flag = ''.join(random.choices(string.ascii_letters + string.digits, k=8)); open('/opt/flag', 'w').write(flag)"

RUN pip install -r requirements.txt
RUN chmod +x ./start.sh

EXPOSE 8000
EXPOSE 22

CMD ./start.sh
