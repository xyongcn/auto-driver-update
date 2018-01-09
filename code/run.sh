#!/bin/bash

echo "autorun.sh running...."

rootDir=~/myProjects
sourceDir=source
filename=net/ethernet/amd/pcnet32.c

if [ $# -ne 1 ];then
  echo "process default filename $sourceDir/$filename"
else 
  if [ -f $sourceDir/$1 ];then # -a -f $2 
    echo "find file $1"
    filename=$1
  else
    echo "input filename $1 is a not correct path name"
    exit 1
  fi
fi

# clean target file
echo "clean target file in path target/"
rm target/*.txt
rm target/*.int
echo ""

#run python file to get interface info--> code/prosInter.py
python code/prosInter.py $sourceDir/$filename".ind"
if [ $? -eq 0 ];then
  echo "python code/prosInter.py $sourceDir/$filename.ind runnning successful."
else
  echo "python code/prosInter.py $sourceDir/$filename.ind runnning faild."
fi
echo ""

:<<!
#make and make clean
cd code  || exit 1
make
if [ $? -eq 0 ];then
  echo "Makefile to make successful."
else
  echo "Makefile to make faild.cannot find any Makefile."
  exit 1
fi
make clean
echo ""
!

#run make result --> main_get
cd $rootDir || exit 1
./code/main_get $sourceDir/$filename
if [ $? -eq 0 ];then
  echo "main_get runnning successful."
else
  echo "main_get runnning faild."
  #exit 1
fi

#run python file to get process headfile --> code/prosHdfile.py 
python code/prosHdfile.py
if [ $? -eq 0 ];then
  echo "python code/prosHdfile.py runnning successful."
else
  echo "python code/prosHdfile.py runnning faild."
fi
echo ""

#run python file --> code/prosDiff.py
python code/prosDiff.py $filename
if [ $? -eq 0 ];then
  echo "python code/prosDiff.py $filename runnning successful."
else
  echo "python code/prosDiff.py $filename runnning faild."
fi
echo ""

echo "autorun.sh running Done."
