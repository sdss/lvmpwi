FROM ubuntu:24.04

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends software-properties-common && \
    apt install -y gnupg ca-certificates && \
    gpg --homedir /tmp --no-default-keyring --keyring /usr/share/keyrings/mono-official-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF && \
    echo "deb [signed-by=/usr/share/keyrings/mono-official-archive-keyring.gpg] https://download.mono-project.com/repo/ubuntu stable-focal main" | tee /etc/apt/sources.list.d/mono-official-stable.list

RUN apt-get update \
    && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        wget \
        wmctrl \
        xfonts-base xfonts-75dpi xfonts-100dpi \
        novnc \
        eterm \
        xrdp \
        libgtk2.0 \
        mono-devel \
        mono-basic-dbg \
        xfce4 xfce4-goodies \
        dbus-x11 \
        xrdp \
        x11-xserver-utils \
        tigervnc-standalone-server \
        python3 \
        pipx

ENV PWI_VERSION=4.1.6final

ENV PWI_PATH=/opt/pwi-$PWI_VERSION
ENV MESA_GL_VERSION_OVERRIDE=4.5

RUN mkdir -p $PWI_PATH && \
    wget http://planewave.com/files/software/PWI4/pwi-$PWI_VERSION.tar.gz && \
    (cd ${PWI_PATH%/*} && tar xzf /pwi-$PWI_VERSION.tar.gz) && \
    rm /pwi-$PWI_VERSION.tar.gz

ENV PWI_AUTOTUNER_VERSION=1.0.3beta1
ENV PWI_AUTOTUNER_PATH=/opt/autotuner-$PWI_AUTOTUNER_VERSION
# beta version of autotuner without 3D
RUN mkdir -p $PWI_AUTOTUNER_PATH && \
    wget http://planewave.com/files/software/PWI4/autotuner-$PWI_AUTOTUNER_VERSION.tar.gz && \
    (cd ${PWI_AUTOTUNER_PATH%/*} && tar xzf /autotuner-$PWI_AUTOTUNER_VERSION.tar.gz) && \
    rm /autotuner-$PWI_AUTOTUNER_VERSION.tar.gz && \
    echo '#!/bin/sh' > $PWI_AUTOTUNER_PATH/run-autotuner_nogl && \
    echo 'cd ${0%/*}' >> $PWI_AUTOTUNER_PATH/run-autotuner_nogl && \
    echo 'mono AutoTuner.exe --nogl' >> $PWI_AUTOTUNER_PATH/run-autotuner_nogl && \
    chmod 755 $PWI_AUTOTUNER_PATH/run-autotuner_nogl

#EXPOSE 3389/tcp
EXPOSE 5900/tcp

WORKDIR /root

RUN mkdir -p lvm/lvmpwi

COPY . lvm/lvmpwi
COPY ./container/run-pwi.sh .
COPY ./container/novnc_server .

RUN cd lvm/lvmpwi && pipx install .

CMD ["/root/run-pwi.sh"]
