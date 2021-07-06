FROM ubuntu:20.04

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

# podman  build --tag ubuntu_lvmt_pwi4 --rm lvmt_pwi4

# podman run --rm -ti --name pwi --network=host -v /home/briegel/workspace/lvmt/lvmpwi:/root/lvmt:Z --device /dev/dri -v ~/.Xauthority:/root/.Xauthority:Z  -e PWI_NAME=pwi localhost/ubuntu_lvmt_pwi

# podman run --rm -ti --name pwi -v /home/briegel/workspace/lvmt/lvmpwi:/root/lvmt:Z -e PWI_NAME=pwi -p 3389 localhost/ubuntu_lvmt_pwi

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
        eterm \
        fluxbox \
        xrdp \
        mono-devel \
        mono-basic-dbg
        
    
EXPOSE 3389/tcp

WORKDIR /root/lvmt

CMD ["/root/lvmt/container/run-pwi.sh"]
