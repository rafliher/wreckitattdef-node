FROM php:7.2-apache

ARG PASSWORD

RUN apt-get update && apt-get install uuid net-tools vim openssh-server -y

# Create ctfuser and set password
RUN useradd -m -d /app ctfuser && echo ctfuser:${PASSWORD} | chpasswd

# Configure SSH for ctfuser
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config && \
    echo "AllowUsers ctfuser" >> /etc/ssh/sshd_config

# Start SSH service
RUN ssh-keygen -A
RUN mkdir -p /run/sshd && chmod 755 /run/sshd

COPY app/ /var/www/html/
COPY flag.txt /flag.txt

RUN chown -R ctfuser:ctfuser /var/www/html/
RUN chown -R www-data:www-data /var/www/html/user
RUN chmod -R 740 /var/www/html/user

COPY start.sh .
RUN chmod +x start.sh

CMD service ssh start && ./start.sh