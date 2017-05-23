#!/usr/bin/python
# python file to get headfile function propertype 

import os
import sys
from subprocess import check_output
from collections import OrderedDict

EXT0 = '.ind' # AST file
EXT2 = '.int' #interface file
SOURCE_PATH0 = '/home/ryyan/SOURCE/linux-3.5.4/'
TARGET_PATH = 'target/' #path to save target file
V0_CODE=sys.argv[1]			#python run param 
FILE_TO_PROCESS = 'console/vgacon.c'

def delSelfFuncCall(count_dict):
 #del self-decl-func call 
  crpath=TARGET_PATH+'cm_list.txt'
  frpath=TARGET_PATH+'func_list.txt'
  func_list=[]
  cm_list=[]
  
  with open(frpath) as fp:
   for line in fp.readlines():
     line = line.rstrip("\n")
     func_list.append(line)
  with open(crpath) as fp:
   for line in fp.readlines():
     line = line.rstrip("\n")
     cm_list.append(line)
  
  temp_list = []
  count = 0
  for cmlist in cm_list:
    funcName=cmlist.split()[1]
    if(funcName not in func_list):
      temp_list.append(cmlist)
    else:
      count += 1
  with open(crpath,'w') as out:
    for tmlist in temp_list:
      print >> out,tmlist
	
  count_dict['call_count'] -= count
  return count_dict
  
def delDuplicateLine(filename):
  #del Duplicate Line in filename
  temp_list = []
  with open(filename) as fp:
   for line in fp.readlines():
     line = line.rstrip("\n")
     if line not in temp_list:
       temp_list.append(line)
  with open(filename,'w') as out:
    for tmlist in temp_list:
      print >> out,tmlist 
       
def mergeCallAndMacro(call_list,macro_list):
  #this function to merge call and macro info 
  lena=len(call_list)
  lenb = len(macro_list)
  cm_list = []
  i=j=0
  while(i<lena and j<lenb):
    clist=call_list[i].split()[-1]
    mlist=macro_list[j].split()[-1]
    flag = cmp(clist,mlist)
    if(flag < 0):
      cm_list.append(call_list[i])
      i+=1
    elif (flag == 0):
      i+=1;
    else:
      cm_list.append(macro_list[j])
      j+=1
  while (i<lena):
	  cm_list.append(call_list[i])
	  i+=1
  while (j<lenb):
	  cm_list.append(macro_list[j])
	  j+=1
  return cm_list

def printListMethod(listname,copath):
  with open(copath, 'a') as out:
    for tlist in listname:
      print >> out,tlist
            
def printToFile(count_dict,call_list,macro_list,sfile_list,macfile_list,isCount):
  copath=TARGET_PATH+'macro_list.txt'
  printListMethod(macro_list,copath)
  copath=TARGET_PATH+'call_list.txt'
  printListMethod(call_list,copath)
  copath=TARGET_PATH+'macfile_list.txt'
  printListMethod(macfile_list,copath)
  delDuplicateLine(copath)
  copath=TARGET_PATH+'sfile_list.txt'
  printListMethod(sfile_list,copath)
  delDuplicateLine(copath)
  copath=TARGET_PATH+'cm_list.txt'
  cm_list = mergeCallAndMacro(call_list,macro_list)  #  merge call and micro
  printListMethod(cm_list,copath) 
   
  if (isCount == 1):
    count_dict['call_count'] += len(cm_list) #count call without pre-complier headfile call
  return count_dict
    
def processFuncDecl(fp, outFname, sline,count_dict):
  ext0 = EXT0
  startLineNo = count_dict['lineNo']
  # get function name,filename and start-end lineno as follows
  nodeNo,tree_type,fnName,tfnFileSno,tfnEno=sline.lstrip().split()   
  if SOURCE_PATH0 in tfnFileSno:  ## add surround if-else 20170520
    fnFileSno=tfnFileSno[len(SOURCE_PATH0):]
  else:
    fnFileSno=tfnFileSno
  fnEno=':'.join(tfnEno.split(':')[1:])
  # get function return type as follows 
  while sline and ("result_decl" not in sline):  
    sline=fp.readline(); count_dict['lineNo'] += 1 #skip line
  else:
    sline=fp.readline(); count_dict['lineNo'] += 1 #skip result_decl line
    tfnType=[]
    while sline and ("parm_decl" not in sline and "bind_expr" not in sline):
      if (len(tfnType) != 0):
        tfnType[-1] = sline.lstrip().split()[-1]+' '+tfnType[-1]
      else:
        tfnType.append(sline.lstrip().split()[-1])
      sline=fp.readline(); count_dict['lineNo'] += 1  
  fnType=tfnType[0]
  for rty in tfnType[1:]:           
    fnType = fnType+' '+rty
  fnType = fnType.strip()
  
  # get function parm as follows
  tfnPara = []  
  while sline and ("bind_expr" not in sline):    
    if sline and ("parm_decl" in sline): 
      sline=fp.readline(); count_dict['lineNo'] += 1  # first identifier_node
      tfnPara.append(' ')  #add new para to save real value
      while sline and ("parm_decl" not in sline and "bind_expr" not in sline):           
        tstr=''
        for s in sline.lstrip().split()[2:]: #change para value
          tstr += s +' ' 
        tstr = tstr.strip()
        if ('(inplace)' not in tstr):
          if cmp(tstr,'*')==0:
            tfnPara[-1] =tstr+tfnPara[-1]
          else:
            tfnPara[-1] =tstr+' '+tfnPara[-1]          
        tfnPara[-1] = tfnPara[-1].strip()
        sline=fp.readline(); count_dict['lineNo'] += 1                    
  if len(tfnPara) > 0 :
    fnPara=tfnPara[0]
    for rty in tfnPara[1:]:                
      fnPara = fnPara+','+rty
    fnPara = fnPara.rstrip()
  else:
    fnPara = ''                   
  
  # get function call info as follows
  call_list = []  # restore called-function
  macro_list = [] # restore called-macro
  macfile_list = []  # restore called-macro and its file relationship
  sfile_list = [] # restore .h of .c file related
  while sline and (sline[0] == ' ' or sline[0] == '\t') and ("function_decl" not in sline):         
    # get Macro Expansion Info    
    if ("_expr" in sline or "indirect_ref" in sline):      
      if (sline.lstrip().split()[-1] != '()'):
        tlist=sline.lstrip().split()
        mlist_sline = fnName+': '+tlist[-2]+' '
        
        if SOURCE_PATH0 in tlist[-1]:  ## add surround if-else 20170520
          mlist_sline = mlist_sline+tlist[-1][:-1][len(SOURCE_PATH0):]
        else:
          mlist_sline = mlist_sline+tlist[-1][:-1]
        if mlist_sline not in macro_list:        	
          macro_list.append(mlist_sline) 
        
        tmfloc = tlist[-3].split('(')[-1].split(':')[:-1]
        if SOURCE_PATH0 in tmfloc[0]: ## add surround if-else 20170520
          mfloc = tlist[-2]+' '+tmfloc[0][len(SOURCE_PATH0):]
        else:
          mfloc = tlist[-2]+' '+tmfloc[0]
        if (mfloc not in macfile_list):        	
          macfile_list.append(mfloc) 
        
        # get .h of which self-called-macro in
        fnFile=fnFileSno.split(':')[0]
        if (fnFile.endswith(os.path.basename(fp.name)[:-len(ext0)])):
          if SOURCE_PATH0 in tmfloc[0]: ## add surround if-else 20170520
            smfloc = tmfloc[0][len(SOURCE_PATH0):]
          else:
            smfloc = tmfloc[0]
          if (smfloc not in sfile_list) and smfloc.endswith('h'):
            sfile_list.append(smfloc) 
        #end              
    if ("call_expr" in sline): # find call location    
      sline_list = sline.lstrip().split()
      fcLoc = sline_list[2]
      sline=fp.readline();count_dict['lineNo'] += 1
      mflag = 1
      if sline and ("component_ref" in sline):
        mflag = 0
      while sline and ("identifier_node" not in sline): 
         sline=fp.readline();count_dict['lineNo'] += 1 #skip lines      
      nodeNo,tree_type,fcName=sline.lstrip().split()      
      if SOURCE_PATH0 in fcLoc: ## add surround if-else 20170520
        tempstr=fnName+': '+fcName+' '+fcLoc[len(SOURCE_PATH0):]
      else:
        tempstr=fnName+': '+fcName+' '+fcLoc
      if mflag and (tempstr not in call_list):
        call_list.append(tempstr)      
    sline=fp.readline();count_dict['lineNo'] += 1

  # print function declation info 
  flag = 1;isCount = 0;
  fnFile=fnFileSno.split(':')[0]
  #restore .h file by the way
  if fnFile.endswith('.h') and (fnFile not in sfile_list):
    sfile_list.append(fnFile)
  
  if (fnFile.endswith(os.path.basename(fp.name)[:-len(ext0)])):
    isCount = 1
    for mlist in macro_list:
      if(mlist.find(fnFileSno) != -1):
        flag = 0;
        break;
    if (flag == 1):
      print >> outFname,'{} {} ({}) {} {} {}'.format(fnType,fnName,fnPara,fnFileSno,fnEno,startLineNo)    
    fcopath=TARGET_PATH+'func_list.txt' 
    count_dict['fndl_count'] += 1
    with open(fcopath, 'a') as out:
      print >> out,'{}'.format(fnName) 
  else:
    print >> outFname,'{} {} ({}) {} {} {}'.format(fnType,fnName,fnPara,fnFileSno,fnEno,startLineNo) 
  
  # print call info
  count_dict=printToFile(count_dict,call_list,macro_list,sfile_list,macfile_list,isCount)                
  fp.seek(-len(sline),1); count_dict['lineNo'] -= 1 #back to last line
  return count_dict
  
def collectIntFmfile(path,outFname):
    count_dict={'fndl_count':0,'lineNo':0,'call_count':0}
    fnCall_dict={}
    with open(path) as fp:
      sline=fp.readline();count_dict['lineNo'] += 1
      while sline:        
        if ((sline[0] != ' ' and sline[0] != '\t') and ("function_decl" in sline)):
          count_dict=processFuncDecl(fp, outFname, sline,count_dict)
        sline=fp.readline();count_dict['lineNo'] += 1
      else:
        count_dict['lineNo'] -= 1
    count_dict=delSelfFuncCall(count_dict)	##del self-func call 
    
    print path,'-->\n\ttotal line',count_dict['lineNo'],'\n\ttotal function decl',count_dict['fndl_count'],'\n\ttotal function call',count_dict['call_count']
    return count_dict['fndl_count']

def collectInt(prefix,outDir):
  ext0=EXT0
  ext2=EXT2 
  global V0_MANIFEST
  #V0_MANIFEST = outDir+'V-'+os.path.split(prefix.strip('/'))[-1]
  V0_MANIFEST = outDir+os.path.split(prefix.strip('/'))[-1]
  if os.path.isfile(V0_CODE):
    assert V0_CODE.endswith(ext0),'file not found with ext *.'+ext0
    print "collect interface info from file-->",os.getcwd()+'/'+V0_CODE
    V0_MANIFEST = V0_MANIFEST[:-len(ext0)]+ext2 
    with open(V0_MANIFEST, 'w') as outFname: #outFname is filename to save func interface
      collectIntFmfile(V0_CODE,outFname)   
  elif os.path.isdir(V0_CODE):
    print "collect interface info from path-->",os.getcwd()+'/'+V0_CODE        
    V0_MANIFEST = V0_MANIFEST+ext2 
    with open(V0_MANIFEST, 'w') as outFname: #outFname is filename to save func interface
      path_list = check_output(['find',prefix,'-name','*'+ext0,'-print0']).rstrip('\0').split('\0')
      fcount = 0
      fncount = 0
      for path in path_list:
        assert path.startswith(prefix) and path.endswith(ext0),'Not found file with ext *.'+ext0
        fcount += 1
        path_code = path[:-len(ext0)]
        filename = path[len(prefix):-len(ext0)].lstrip('/')
        fncount += collectIntFmfile(path,outFname) 
    print prefix,"-->\n\ttotal .ind file",fcount,"\n\ttotal function decl",fncount
  print 'collectInt():V0_MANIFEST-->',V0_MANIFEST 

def reviseHdFile(vers):
  outpath = TARGET_PATH+'v'+vers+'_headfile.txt'
  inpath = TARGET_PATH+'sfile_list.txt'
  str1 = 'arch/x86/include/'
  str2 = 'include/'
  
  hfile_list = [] #
  with open(outpath) as fp:
    for line in fp.readlines():
      line = line.rstrip('\n')
      hfile_list.append(line)
  with open(inpath) as fp:
    for line in fp.readlines():
      line = line.rstrip('\n')
      if line.startswith(str1):
        line = line[len(str1):]
      else:
        line = line[len(str2):] 
      if line not in hfile_list:
        hfile_list.append(line)
  with open(outpath,'w') as out:
    for tlist in hfile_list:
      print >> out,tlist
      
  #if (cmp(vers,'1') ==0) and os.path.isfile(inpath):
  #  os.remove(inpath)
  print 'revise',outpath,'successful.'
  
def info_collect():
    ext0=EXT0
    ext2=EXT2
   
    if (os.path.exists('target') == False) or (os.path.isdir('target') == False):
        os.mkdir("target")
    print "target path to save info-->",os.getcwd()+'/'+TARGET_PATH
    
    if os.path.exists(V0_CODE):
        if os.path.isfile(TARGET_PATH+'func_list.txt'): # if file exist then del
            os.remove(TARGET_PATH+'func_list.txt') 
        if os.path.isfile(TARGET_PATH+'macro_list.txt'): # if file exist then del
            os.remove(TARGET_PATH+'macro_list.txt')
        if os.path.isfile(TARGET_PATH+'call_list.txt'): # if file exist then del
            os.remove(TARGET_PATH+'call_list.txt')
        if os.path.isfile(TARGET_PATH+'cm_list.txt'): # if file exist then del
            os.remove(TARGET_PATH+'cm_list.txt')
        if os.path.isfile(TARGET_PATH+'macfile_list.txt'): # if file exist then del
            os.remove(TARGET_PATH+'macfile_list.txt')
        # call function to collect interface infomattion
        collectInt(V0_CODE,TARGET_PATH)       
    else:
        print "cannot find path or file",V0_CODE
        
def main():
    print 'python file:',sys.argv[0],'running...'
    print 'input file:',sys.argv[1]
    info_collect()
    reviseHdFile('0')
    reviseHdFile('1')
    print 'Done'
  
if __name__ == '__main__':
    main()
