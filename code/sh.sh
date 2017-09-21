#!/bin/bash

echo "sh.sh running ..."

rootDir=~/myProjects
srcpath=~/SOURCE/
kernpath=linux-3.5.6/drivers
kernpath2=linux-3.8.13/drivers
targetpath=~/myProjects/assitLog

filelist=`find source/ -name *.c`
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
echo "sh.sh running done."
