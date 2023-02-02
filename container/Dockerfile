FROM ubuntu:22.04

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de


# podman  build --tag ubuntu_lvmt_pwi4 --rm lvmt_pwi4

# podman run --rm -ti --name pwi --network=host -v /home/briegel/workspace/lvmt/lvmpwi:/root/lvmt:Z --device /dev/dri -v ~/.Xauthority:/root/.Xauthority:Z  -e PWI_NAME=pwi localhost/ubuntu_lvmt_pwi

# podman run --rm -ti --name pwi -v /home/briegel/workspace/lvmt/lvmpwi:/root/lvmt:Z -e PWI_NAME=pwi -p 3389 localhost/ubuntu_lvmt_pwi

# podman run --rm -ti --name lvm-sci-pwi -v ~lvm/workspace/lvm:/root/lvm:Z -e PWI_NAME=lvm.sci.pwi -e PWI_GEOM=1200x900 -e LVM_ACTOR_ARGS="--verbose --rmq_url=amqp://guest:guest@192.168.1.1:5672/" -p 8091:6080 ghcr.io/sdss/lvmpwi:latest

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends software-properties-common && \
    apt install -y gnupg ca-certificates && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF && \
    echo "deb https://download.mono-project.com/repo/ubuntu stable-focal main" | tee /etc/apt/sources.list.d/mono-official-stable.list 


# RUN dpkg --add-architecture i386 && \
#     wget -qO- https://dl.winehq.org/wine-builds/winehq.key | sudo apt-key add - && \
#     apt-add-repository "deb http://dl.winehq.org/wine-builds/ubuntu/ $(lsb_release -cs) main" && \
#     apt install -y --install-recommends winehq-stable winetricks


RUN apt-get update \
    && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        wget \
        wmctrl \
        xfonts-base xfonts-75dpi xfonts-100dpi \
        tightvncserver \
        novnc \
        eterm \
        fluxbox \
        xrdp \
        libgtk2.0 \
        mono-devel \
        mono-basic-dbg

RUN apt install -y python3-pip

RUN pip3 install sdss-lvmpwi

#ENV PWI_VERSION=4.0.9beta21
ENV PWI_VERSION=4.0.11beta50
#ENV PWI_VERSION=4.0.13final
ENV PWI_PATH=/opt/pwi-$PWI_VERSION

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

COPY ./container/run-pwi.sh .
COPY ./container/novnc_server .

CMD ["/root/run-pwi.sh"]

