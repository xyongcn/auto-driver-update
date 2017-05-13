#!/bin/bash

echo "autorun.sh running...."

rootDir=~/myProjects
sourceDir=source
filename=console/vgacon.c

#make and make clean
cd code  || exit 1
make
if [ $? -eq 0 ];then
  echo "Makefile to make successful."
else
  echo "Makefile to make faild."
  exit 1
fi
make clean

#run make result --> main_get
cd $rootDir || exit 1
./code/main_get $sourceDir/$filename
if [ $? -eq 0 ];then
  echo "main_get runnning successful."
else
  echo "main_get runnning faild."
  exit 1
fi

#run python file to get interface info--> code/prosInter.py
python code/prosInter.py $sourceDir/$filename".ind"
if [ $? -eq 0 ];then
  echo "python code/prosInter.py $sourceDir/$filename.ind runnning successful."
else
  echo "python code/prosInter.py $sourceDir/$filename.ind runnning faild."
fi

#run python file to get process headfile --> code/prosHdfile.py
tgfnm1=$rootDir/target/hfileList.txt 
python code/prosHdfile.py $tgfnm1
if [ $? -eq 0 ];then
  echo "python code/prosHdfile.py $tgfnm1 runnning successful."
else
  echo "python code/prosHdfile.py $tgfnm1 runnning faild."
fi

#run python file --> code/prosDiff.py
python code/prosDiff.py $filename
if [ $? -eq 0 ];then
  echo "python code/prosDiff.py $filename runnning successful."
else
  echo "python code/prosDiff.py $filename runnning faild."
fi

echo -e "\nautorun.sh Done."
