FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8 && \
    apt update && \
    apt install -y libjpeg-dev zlib1g-dev python3-dev build-essential \
    libpcre3 libpcre3-dev libxml2 libxslt-dev
COPY ./requirements.txt ./requirements.txt

WORKDIR /src/


COPY ./app /src

COPY requirements.txt .
RUN pip install pip --upgrade
RUN pip install --require-hashes -r requirements.txt

RUN useradd -ms /bin/bash user

RUN chown -R user:user /src && \
    chmod -R 775 /src/

USER user
