FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app/

RUN apt-get update && apt-get install -y gnupg software-properties-common && \
    apt install wget -y && \
    wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    tee /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    gpg --no-default-keyring \
    --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    --fingerprint && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list && \
    apt update && \
    apt-get install terraform -y

CMD ["./bootstrap.sh"]


# '''
# apt-get update && apt-get install -y gnupg software-properties-common

# apt install wget -y

# wget -O- https://apt.releases.hashicorp.com/gpg | \
# gpg --dearmor | \
# tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

# gpg --no-default-keyring \
# --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
# --fingerprint

# echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
# https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
# tee /etc/apt/sources.list.d/hashicorp.list

# apt update

# apt-get install terraform -y

# '''