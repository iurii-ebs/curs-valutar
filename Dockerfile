FROM python:3.8
ARG DEBIAN_FRONTEND=noninteractive

# Install missing libs
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -y curl wget git

# Install wkhtmltopdf
RUN apt-get install -f -y xvfb libfontconfig wkhtmltopdf
RUN ln -s /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf

# Creating Application Source Code Directory
RUN mkdir -p /usr/app

# Setting Home Directory for containers
WORKDIR /usr/app

# Installing python dependencies
COPY . /usr/app
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Exposing Ports
EXPOSE 8000 8014 8015
