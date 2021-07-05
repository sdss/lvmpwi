#!/usr/bin/bash -l

LVMT_PATH=/root/lvmt
LVMT_CONFIG_PATH=$LVMT_PATH/config/lvm/$PWI_NAME

PATH=$LVMT_PATH/scripts:$PATH
PYTHONPATH=$LVMT_PATH/python/:$PYTHONPATH

PWI_VERSION=4.0.9beta21

if [ ! -d $LVMT_PATH/pwi-$PWI_VERSION ]; then
  mkdir -p $LVMT_PATH/3rdparty/
  test -e $LVMT_PATH/3rdparty/pwi-$PWI_VERSION.tar.gz || wget http://planewave.com/files/software/PWI4/pwi-$PWI_VERSION.tar.gz -O $LVMT_PATH/3rdparty/pwi-$PWI_VERSION.tar.gz
  echo unpacking ...
  (cd $LVMT_PATH/ && tar xzf $LVMT_PATH/3rdparty/pwi-$PWI_VERSION.tar.gz)
fi


mkdir -p ~/PlaneWave\ Instruments/PWI4/
rm -rf ~/PlaneWave\ Instruments/PWI4/Settings
(cd ~/PlaneWave\ Instruments/PWI4/ && ln -s $LVMT_CONFIG_PATH/PWI4/Settings/ )
(cd ~/lvmt/pwi-$PWI_VERSION/ && ./run-pwi4&)
