FROM --platform=amd64 archlinux:latest
WORKDIR /root
COPY internal-scripts ./internal-scripts
RUN bash internal-scripts/init-image.sh && rm -r internal-scripts
USER builder
WORKDIR /home/builder
COPY gnupg.tar.gz .
RUN tar -xf gnupg.tar.gz && rm gnupg.tar.gz
COPY internal-scripts/init-repoctl.sh .
RUN bash init-repoctl.sh && rm init-repoctl.sh
COPY pkgbuilder ./pkgbuilder
