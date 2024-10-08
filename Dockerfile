FROM python:3.12.3


WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
EXPOSE 8000
