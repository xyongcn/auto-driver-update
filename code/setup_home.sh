#!/bin/bash

echo "run.sh running...."

cd ~/SOURCE
if [ -d linux-3.5.4/ ];then
  rm -r linux-3.5.4/
fi
if [ -d linux-3.8.13/ ];then
  rm -r linux-3.8.13/
fi
if [ -d build-linux-v0/ ];then
  rm -r build-linux-v0/
fi
if [ -d build-linux-v1/ ];then
  rm -r build-linux-v1/
fi

echo "tar file linux-3.5.3..."
tar xf ~/Downloads/linux-3.5.4.tar.bz2
echo "tar file linux-3.8.13..."
tar xf ~/Downloads/linux-3.8.13.tar.bz2
if [ $? -eq 0 ];then
  echo "tar successful."
else
  echo "tar faild."
  exit 1
fi

echo "create build folder in ~/SOURCE"
mkdir ~/SOURCE/build-linux-v0
mkdir ~/SOURCE/build-linux-v1


cd ~/SOURCE/linux-3.5.4/
make O=~/SOURCE/build-linux-v0 V=1 allnoconfig
make O=~/SOURCE/build-linux-v0 V=1 menuconfig
echo "complier kernel source linux-3.5.4..."
time make O=~/SOURCE/build-linux-v0 V=1 EXTRA_CFLAGS="-fplugin=gccdiff" > ~/SOURCE/dummy5 2>&1
ret=`find . -name "*.ind"`
if [ x"$ret" == x"" ];then
  echo "complier again..."
  time make O=~/SOURCE/build-linux-v0 V=1 EXTRA_CFLAGS="-fplugin=gccdiff" > ~/SOURCE/dummy5 2>&1
else
  echo "creat .ind file in linux-3.5.4  successful."
fi

cd ~/SOURCE/linux-3.8.13/
make O=~/SOURCE/build-linux-v1 V=1 allnoconfig
make O=~/SOURCE/build-linux-v1 V=1 menuconfig
echo "complier kernel source linux-3.8.13..."
time make O=~/SOURCE/build-linux-v1 V=1 > ~/SOURCE/dummy8 2>&1
ret=`find . -name *.ind`
if [ x"$ret" == x"" ];then
  echo "complier again..."
  time make O=~/SOURCE/build-linux-v1 V=1 > ~/SOURCE/dummy5 2>&1
else
  echo "creat .ind file in linux-3.8.13  successful."
fi

echo "Done."
