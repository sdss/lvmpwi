FROM ubuntu:20.04

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

# podman  build --tag ubuntu_lvmt_pwi4 --rm lvmt_pwi4

# podman run -ti --rm --name lvmt_pwi4 -e DISPLAY --network=host --ipc=host --device /dev/dri -v ~/.Xauthority:/root/.Xauthority:Z -v .:/root/lvmt:Z -P localhost/ubuntu_lvmt_pwi4

RUN apt update -y && \
    apt install -y wget && \
    echo "8\n7\n" | apt install -y software-properties-common && \
    echo "30\n1\n" | apt install -y keyboard-configuration && \
    apt install -y sudo subversion git lsof && \
    apt update -y

# RUN dpkg --add-architecture i386 && \
#     wget -qO- https://dl.winehq.org/wine-builds/winehq.key | sudo apt-key add - && \
#     apt-add-repository "deb http://dl.winehq.org/wine-builds/ubuntu/ $(lsb_release -cs) main" && \
#     apt install -y --install-recommends winehq-stable winetricks

RUN apt install gnupg ca-certificates && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF && \
    echo "deb https://download.mono-project.com/repo/ubuntu stable-focal main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list && \
    apt update -y && \
    apt install -y mono-devel mono-basic-dbg

WORKDIR /root/lvmt

CMD ["/root/lvmt/container/run-pwi.sh"]

