FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    autoconf gcc make git libcurl4-openssl-dev \
    libncurses5-dev libtool libjansson-dev libudev-dev libusb-1.0-0-dev \
    && apt-get clean

WORKDIR /app

COPY miner.py /app/miner.py

CMD ["python3", "/app/miner.py"]
