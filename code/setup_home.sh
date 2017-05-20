#!/bin/bash

echo "run.sh running...."

cd ~/SOURCE
rm -r linux-3.5.4/
rm -r linux-3.8.13/
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
mkdir ~/SOURCE/build-l5-allno
mkdir ~/SOURCE/build-l8-allno


cd ~/SOURCE/linux-3.5.4/
make O=~/SOURCE/build-l5-allno V=1 localmodconfig
make O=~/SOURCE/build-l5-allno V=1 menuconfig
echo "complier kernel source linux-3.5.4..."
time make O=~/SOURCE/build-l5-allno V=1 EXTRA_CFLAGS="-fplugin=gccdiff" > ~/SOURCE/dummy5 2>&1
ret=`find . -name "*.ind"`
if [ x"$ret" == x"" ];then
  echo "complier again..."
  time make O=~/SOURCE/build-l5-allno V=1 EXTRA_CFLAGS="-fplugin=gccdiff" > ~/SOURCE/dummy5 2>&1
else
  echo "creat .ind file in linux-3.5.4  successful."
fi

cd ~/SOURCE/linux-3.8.13/
make O=~/SOURCE/build-l8-allno V=1 allnoconfig
echo "complier kernel source linux-3.8.13..."
time make O=~/SOURCE/build-l8-allno V=1 EXTRA_CFLAGS="-fplugin=gccdiff" > ~/SOURCE/dummy8 2>&1
ret=`find . -name *.ind`
if [ x"$ret" == x"" ];then
  echo "complier again..."
  time make O=~/SOURCE/build-l8-allno V=1 EXTRA_CFLAGS="-fplugin=gccdiff" > ~/SOURCE/dummy5 2>&1
else
  echo "creat .ind file in linux-3.8.13  successful."
fi

echo "Done."
