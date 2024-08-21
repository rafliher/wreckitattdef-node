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

# Generate SSH host keys
RUN ssh-keygen -A

# Ensure /run/sshd directory exists with correct permissions
RUN mkdir -p /run/sshd && chmod 755 /run/sshd

# Copy source code and set permissions
COPY src/ /var/www/html
RUN mkdir /var/www/html/backups && \
    chown -R ctfuser:ctfuser /var/www/html && \
    chmod -R 777 /var/www/html

# Allow URL inclusion in PHP
RUN echo "allow_url_include = On" >> /usr/local/etc/php/php.ini

# Copy start script and set execute permissions
COPY start.sh .
RUN chmod +x start.sh

# Start SSH service as root and then switch to ctfuser
CMD service ssh start && ./start.sh

