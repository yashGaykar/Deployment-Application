FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["./bootstrap.sh"]
