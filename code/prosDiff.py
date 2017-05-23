#!/usr/bin/python
# python file to get assistant infomation

import os
import sys
import commands
from subprocess import check_output
from collections import OrderedDict

EXT0 = '.ind' # AST file
EXT2 = '.int' #interface file
SOURCE_PATH0 = os.environ['HOME']+'/SOURCE/linux-3.5.4/'
SOURCE_PATH1 = os.environ['HOME']+'/SOURCE/linux-3.8.13/'
TARGET_PATH = 'target/' #path to save target file
FILE_TO_PROCESS = sys.argv[1]
CTAGSFILE_EXT = '_ctags.txt'
LOGERR = 'log.txt'

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
        if _type in ('macro','function','prototype'):
          ctags_dict[name] = [_type,rows,_file,statement]
      sline = fp.readline()
  return ctags_dict

def prosTargetf():
  fnFile_dict = getFuncAndFile()
  fnCall_dict = getFuncCallDict(FILE_TO_PROCESS)
  v0ctags_dict = getCtagsFileDict('0')
  
  fcFile_dict = OrderedDict()
  for fnName in fnCall_dict.keys():
    if fnName in v0ctags_dict:
      fcFile_dict[fnName] = v0ctags_dict[fnName]
    elif fnName in fnFile_dict:  #comthing wrong occured here,need to solve
      # macro define function
      tlist = fnFile_dict[fnName][0].split(':')
      fileph = SOURCE_PATH0+tlist[0]
      rows =  tlist[1]
      Sno = tlist[1]+':'+tlist[2]
      Eno = fnFile_dict[fnName][1]
      tstr=check_output(['sed','-n',rows+'p',fileph]).strip()
      if cmp(Sno,Eno)==0:
        fcFile_dict[fnName] =['macfun'] + tlist[:-1] + [tstr]
      else:
        fcFile_dict[fnName] =['function'] + tlist[:-1] + [tstr]
    #else:  # if not found,may self-decl-macro or kenerl-decl macro of func
    #  fcFile_dict[fnName] = []
  #print To File
  printToFile(fnFile_dict,fnCall_dict,fcFile_dict)
  return fcFile_dict

def code_Diff():
  v0ctags_dict = getCtagsFileDict('0')
  v1ctags_dict = getCtagsFileDict('1') 
  diffLog_dict = OrderedDict()
  for k,vlist in v0ctags_dict.items():
    v0_type,v0_file,v0_rows,v0_state = vlist[0:]
    if v0_type not in ('struct','member'):
      if k in v1ctags_dict:# if exist
        v1_type,v1_file,v1_rows,v1_state = v1ctags_dict[k]
        if cmp(v0_file,v1_file)==0:       
          if (cmp(v0_type,v1_type)==0) and (cmp(v0_state,v1_state)==0): 
            #nothing changed
            diffLog_dict[k] = ['Not']
            del v1ctags_dict[k]
          else: 
            #decl changed
            if cmp(v0_type,v1_type)!=0:
              cstr = v0_type+'-->'+v1_type
            else:
              cstr = v0_type
            diffLog_dict[k] = ['Mod',cstr,v0_file,v0_state,v1_state]
            del v1ctags_dict[k]
        else:
          if (cmp(v0_type,v1_type)==0) and (cmp(v0_state,v1_state)==0):
            #just file changed
            diffLog_dict[k] = ['Mov',v1_type,v0_file,v1_file,v1_state]
            del v1ctags_dict[k]
          else:
            #all changed(file,decl)
            _file = v0_file+'-->'+v1_file #file
            if cmp(v0_type,v1_type)!=0:   #type
              _type = v0_type+'-->'+v1_type
            else:
              _type = v0_type
            diffLog_dict[k] = ['All',_type,_file,v0_state,v1_state]
            del v1ctags_dict[k]
      else: 
        # not exist-->deleted
        diffLog_dict[k] = ['Del',v0_type,v0_file,v0_state]  
    else: # struct typedef and so on
      pass 
  if len(v1ctags_dict)>0:
    # add changed
    for k,vlist in v1ctags_dict.items():
      diffLog_dict[k] = ['Add'] + vlist 
  return diffLog_dict

def classDiffLog(diffLog_dict):
  Alevel_dict = OrderedDict() # impact
  Blevel_dict = OrderedDict() # impact value
  Clevel_dict = OrderedDict() # little impact
  for k,vlist in diffLog_dict.items():
    diff_type = vlist[0]
    if diff_type in ('Not','Mov'):
      pass
    elif cmp(diff_type,'Del')==0:
      Alevel_dict[k] = diffLog_dict[k]
    elif diff_type in ('Mod','All'):  
      _type,_file,v0_state,v1_state = vlist[1:]
      if '-->' not in _type: #type not changed
        if cmp(_type,'macro')!=0:
          Alevel_dict[k] = diffLog_dict[k]
        else: 
          macor_name_list = v0_state.split()
          if('(' in macor_name_list[1]): # macro with parameter
            state0 = v0_state.split(k)[1].split(')')[0]+')'
            state1 = v1_state.split(k)[1].split(')')[0]+')'
            if(cmp(state0,state1)==0):
              Blevel_dict[k] = diffLog_dict[k]
            else:
              Alevel_dict[k] = diffLog_dict[k]
          else: # macro without parameter
            Blevel_dict[k] = diffLog_dict[k]
      else: #type changed,but defination may not changed
        state0 = v0_state.split(k)[1].rstrip(';')
        state1 = v1_state.split(k)[1].rstrip(';')
        if cmp(state0,state1)==0:
          Clevel_dict[k] = diffLog_dict[k]
        else:
          Alevel_dict[k] = diffLog_dict[k]
    else: # cmp(diff_type,'Add')==0
      pass 
  return Alevel_dict,Blevel_dict,Clevel_dict
  
def getAssitInfo():
  diffLog_dict = code_Diff()
  fcFile_dict = prosTargetf()
  Alevel_dict,Blevel_dict,Clevel_dict = classDiffLog(diffLog_dict)
  assitInfo_dict = OrderedDict()
  for k,vlist in fcFile_dict.items():
    _type,_file,_rows,state = vlist[0:]
    if k in diffLog_dict:
      assitInfo_dict[k] = diffLog_dict[k]
    else: # macro define function condition
      fileph = SOURCE_PATH1 + _file
      cmd_string = "grep -w '"+state+"' "+fileph
      tstr=commands.getstatusoutput(cmd_string)
      if tstr[0] == 0 and cmp(state,tstr[1]) ==0 :
        assitInfo_dict[k] = ['Not']
      else:
      	cname = state.split('(')[0]
      	if cname in diffLog_dict:
      	  assitInfo_dict[k] = diffLog_dict[cname]
      	else:
          assitInfo_dict[k] = ['Del']+[_type,_file,state]
  
  for k,v in assitInfo_dict.items():
    print k,v 
  
  with open(LOGERR,'w') as out:
    print >> out,'\n------A level difference--------------\n'
    for k,vlist in Alevel_dict.items():
      print >> out,k,vlist
    print >> out,'\n------B level difference--------------\n'
    for k,vlist in Blevel_dict.items():
      print >> out,k,vlist
    print >> out,'\n------C level difference--------------\n'
    for k,vlist in Clevel_dict.items():
      print >> out,k,vlist
    
def main():
    print '\npython file:',sys.argv[0],'running...'
    print 'input file:',sys.argv[1]
    getAssitInfo()
    print 'Done\n'
  
if __name__ == '__main__':
    main()
