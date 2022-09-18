FROM python:3.9.10-slim-buster as note-app-api

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Setup linux dependencies
RUN apt-get update && apt-get install -y \
    logrotate wget curl \
    nano vim less

# create the appropriate directories
ENV APP_HOME=/home/app
WORKDIR $APP_HOME
RUN mkdir $APP_HOME/logs

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip wheel setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Copy application codes into docker
COPY . $APP_HOME

# Create user, group and change owner
RUN adduser -u 1001 --disabled-password --gecos "" app && \
    chown -R app:app $HOME

# change to the app user
USER app

# Open the mapped port
EXPOSE 8000

CMD ["uvicorn", "main:app" ,"--reload"]