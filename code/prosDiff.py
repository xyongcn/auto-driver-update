#!/usr/bin/python
# python file to get interface infomation

import os
import sys
from subprocess import check_output
from collections import OrderedDict

EXT0 = '.ind' # AST file
EXT2 = '.int' #interface file
SOURCE_PATH0 = os.environ['HOME']+'/SOURCE/linux-3.5.4/'
TARGET_PATH = 'target/' #path to save target file
FILE_TO_PROCESS = sys.argv[1]
CTAGSFILE_EXT = '_ctags.txt'

def printDictMethod(dictname,filename):
  with open(filename,'w') as out:
    for (k,v) in dictname.items():
      print >> out,k,v

def printToFile(fnFile_dict,fnCall_dict,fcFile_dict):
  fnFilePath = TARGET_PATH + 'fnFileTemp.txt'
  printDictMethod(fnFile_dict,fnFilePath)
  print 'generated file:',fnFilePath
  
  fnCallPath = TARGET_PATH + 'fnCallTemp.txt'
  with open(fnCallPath,'w') as out:
		for fnName,fcName_dict in fnCall_dict.items():
		  print >> out,fnName
		  for fcName,fcLoc_list in fcName_dict.items():
		    print >> out,'  '+fcName
		    for fcLoc in fcLoc_list:
		      print >> out,'    '+fcLoc
  print 'generated file:',fnCallPath
  
  fcFilePath = TARGET_PATH + 'fcFileTemp.txt'
  printDictMethod(fcFile_dict,fcFilePath)
  print 'generated file:',fcFilePath
'''
def getMacAndFile():
  #get macro-file like {'macroName':['file:sloc']}}
  rpath = TARGET_PATH+'macfile_list.txt'
  macFile_dict = OrderedDict()
  with open(rpath) as fp:
    sline=fp.readline();
    while sline:    
      macName,macFile = sline.split()
      if macName not in macFile_dict:
        macFile_dict[macName] = macFile
      sline=fp.readline();
  return macFile_dict
''' 
def getFuncAndFile():
  #get func-file like {'fnName':['file:sloc','eloc','.ind--lineNo']}}
  #V0_MANIFEST
  rpath = check_output(['find',TARGET_PATH,'-name','*'+EXT2]).rstrip('\n')
  fnFile_dict = OrderedDict()
  linec = 0
  with open(rpath) as fp:
    sline=fp.readline();linec += 1
    while sline:    
      left,right = sline.split('(')
      fnName = left.strip().split()[-1]
      rright = right.split(')')[-1]
      fnFile = rright.strip().split()[:-1]
      if fnName not in fnFile_dict:
        fnFile_dict[fnName] = fnFile
      sline=fp.readline();linec += 1
  return fnFile_dict
 
def getFuncCallDict(filename):
  #get func-call-dict like {'fdA':{'fcB':['loc1','loc2']}}
  #filename = os.path.basename(path)[:-len(EXT2)]
  crpath=TARGET_PATH+'cm_list.txt'
  fnCall_dict = OrderedDict()
  with open(crpath) as fp:
    sline=fp.readline();
    while sline:
      fnName,fcName,fcLoc=sline.split()
      if fcLoc.split(':')[0].endswith(os.path.basename(filename)):
		    if fcName not in fnCall_dict:
		      fnCall_dict[fcName]=OrderedDict()
		      fnCall_dict[fcName][fnName]=[fcLoc]
		    else:
		      if fnName not in fnCall_dict[fcName]:
		        fnCall_dict[fcName][fnName]=[fcLoc]
		      else:
		        fnCall_dict[fcName][fnName].append(fcLoc)
      sline=fp.readline();
  return fnCall_dict

def getCtagsFileDict(vers):
  filename = TARGET_PATH+'v'+vers+CTAGSFILE_EXT
  ctags_dict = OrderedDict()
  with open(filename) as fp:
    sline = fp.readline()
    while sline:
      if (sline !='\n' ):
        tlist = sline.split()
        name = tlist[0]
        _type = tlist[1]
        rows = tlist[2]
        _file = tlist[3]
        statement = ' '.join(tlist[4:])
        ctags_dict[name] = [_type,rows,_file,statement]
      sline = fp.readline()
  return ctags_dict

def prosTargetf():
  fnFile_dict = getFuncAndFile()
  #macFile_dict= getMacAndFile()
  fnCall_dict = getFuncCallDict(FILE_TO_PROCESS)
  
  v0ctags_dict = getCtagsFileDict('0')
  v1ctags_dict = getCtagsFileDict('1')
  #ctags_dict[name] = [_type,rows,_file,statement]
  
  fcFile_dict = OrderedDict()
  for fnName in fnCall_dict.keys():
    if fnName in v0ctags_dict:
      fcFile_dict[fnName] = v0ctags_dict[fnName]
    elif fnName in fnFile_dict:
      # macro define function
      tlist = fnFile_dict[fnName][0].split(':')
      fileph = SOURCE_PATH0+tlist[0]
      rows =  tlist[1]
      tstr=check_output(['sed','-n',rows+'p',fileph]).strip()
      fcFile_dict[fnName] =['macfun'] + tlist[:-1] + [tstr]
    else:
      fcFile_dict[fnName] = []
  #print To File
  printToFile(fnFile_dict,fnCall_dict,fcFile_dict)
 # return fnFile_dict,macFile_dict,fnCall_dict,fcFile_dict

#def code_Diff():
  
def main():
    print '\npython file:',sys.argv[0],'running...'
    print 'input file:',sys.argv[1]
    prosTargetf()
    print 'Done'
  
if __name__ == '__main__':
    main()
