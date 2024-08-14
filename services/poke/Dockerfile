FROM public.ecr.aws/docker/library/php:8.0-apache

ARG PASSWORD

# Create ctfuser and set password
RUN useradd -m -d /var/www/html ctfuser && echo ctfuser:${PASSWORD} | chpasswd

# Install necessary packages
RUN apt-get update && apt-get install -y openssh-server curl

# Configure SSH for ctfuser
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config && \
    echo "AllowUsers ctfuser" >> /etc/ssh/sshd_config

# Start SSH service
RUN service ssh start

# Copy source code and set permissions
COPY src/ /var/www/html
RUN mkdir /var/www/html/backups && \
    chown -R www-data:www-data /var/www/html/backups && \
    chmod -R 777 /var/www/html/backups

# Allow URL inclusion in PHP
RUN echo "allow_url_include = On" >> /usr/local/etc/php/php.ini

# Copy start script and set execute permissions
COPY start.sh .
RUN chmod +x start.sh

# Set ctfuser as the default user
USER ctfuser

# Start the application
CMD ./start.sh
