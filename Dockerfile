FROM python:3.8

# Install missing libs
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -y curl wget git

# Install wkhtmltopdf
RUN apt-get install -f -y xvfb libfontconfig xfonts-75dpi wkhtmltopdf
RUN ln -s /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb
RUN apt-get -f -y install
RUN apt-get -y autoremove

# Creating Application Source Code Directory
RUN mkdir -p /usr/app

# Setting Home Directory for containers
WORKDIR /usr/app

# Installing python dependencies
COPY . /usr/app
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Collect static files
RUN python manage.py collectstatic --noinput

# Exposing Ports
EXPOSE 5432 8015
