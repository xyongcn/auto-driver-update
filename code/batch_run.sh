#!/bin/bash

echo "batch_run.sh running ..."
if [ -f runlog.txt ];then
  rm runlog.txt
fi
touch runlog.txt
echo "create log file runlog.txt."

echo "clean target file in path assitLog/"
rm assitLog/*

filelist=`find source/ -name *.c`
for filename in $filelist ;do
  filename=${filename#*/}
  echo "processing file $filename ..."
  source code/run.sh $filename >> runlog.txt
  echo "Done."
done

# get diff patch of two c source file
rootDir=~/myProjects
srcpath=~/SOURCE/
kernpath=linux-3.5.6/drivers
kernpath2=linux-3.8.13/drivers
targetpath=~/myProjects/assitLog

echo "srcpath:$srcpath"
cd $srcpath || exit 1
for filename in $filelist ;do
  filename=${filename#*/}
  fname=$(basename $filename)
  echo "processing file $filename ..."
  path=$kernpath/$filename
  path2=$kernpath2/$filename
  if [ -f $path ];then
    echo "find path:$path"
    echo "find path:$path2"
    diff -Naur $path $path2 > $targetpath/$fname"_diff.patch"
  else
    echo "cannot find path:$path"
  fi 
  echo ""
done
cd $rootDir || exit 1

echo "batch_run.sh running done."
