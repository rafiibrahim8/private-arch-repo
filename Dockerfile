FROM --platform=amd64 archlinux:latest
WORKDIR /root
COPY internal-scripts/init-image.sh .
RUN bash init-image.sh
USER builder
WORKDIR /home/builder
COPY gnupg.tar.gz .
RUN tar -xf gnupg.tar.gz
