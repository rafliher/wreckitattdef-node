FROM php:7.2-apache

ENV PASS=useruseruser

RUN apt-get update && apt-get install uuid net-tools vim openssh-server -y

COPY app/ /var/www/html/
COPY flag.txt /flag.txt

RUN useradd user -s /bin/bash && echo "user:$PASS" | chpasswd

RUN chown -R user:user /var/www/html/
RUN chown -R www-data:www-data /var/www/html/user
RUN chmod -R 740 /var/www/html/user
