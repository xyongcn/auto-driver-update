# -*- coding: UTF-8 -*-

'''
 To get interface infomation
'''

import os
import sys
from subprocess import check_output
from collections import OrderedDict

EXT0 = '.ind' # AST file
EXT2 = '.int' #interface file
SOURCE_PATH0 = '/tmp/linux-3.5.4'
  
def delSelfFuncCall(targetPath,count_dict):
 #del self-decl-func call 
  crpath=targetPath+'/cm_list.txt'
  frpath=targetPath+'/func_list.txt'
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
      #cm_list.append(macro_list[j])
      i+=1;#j+=1
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

def getFuncCallDict(targetPath,path):
  #get func-call-dict like {'fdA':{'fcB':['loc1','loc2']}}
  filename = os.path.basename(path)[:-len(EXT2)]
  crpath=targetPath+'/cm_list.txt'
  fnCall_dict = OrderedDict()
  with open(crpath) as fp:
    sline=fp.readline();
    while sline:
      fnName=sline.split()[0]
      fcName=sline.split()[1]
      fcLoc =sline.split()[2]
      if fcLoc.split(':')[0].endswith(filename):
		    if fnName not in fnCall_dict:
		      fnCall_dict[fnName]=OrderedDict()
		      fnCall_dict[fnName][fcName]=[fcLoc]
		    else:
		      if fcName not in fnCall_dict[fnName]:
		        fnCall_dict[fnName][fcName]=[fcLoc]
		      else:
		        fnCall_dict[fnName][fcName].append(fcLoc)
      sline=fp.readline();
  return fnCall_dict

def printMethod(listname,copath):
  with open(copath, 'a') as out:
    for tlist in listname:
      print >> out,tlist
            
def printToFile(outFname,count_dict,call_list,macro_list,file_list,isCount):
  copath=os.path.dirname(outFname.name)+'/macro_list.txt'
  printMethod(macro_list,copath)
  copath=os.path.dirname(outFname.name)+'/call_list.txt'
  printMethod(call_list,copath)
  copath=os.path.dirname(outFname.name)+'/file_list.txt'
  printMethod(file_list,copath)
  delDuplicateLine(copath)
  copath=os.path.dirname(outFname.name)+'/cm_list.txt'
  cm_list = mergeCallAndMacro(call_list,macro_list)  #  merge call and micro
  printMethod(cm_list,copath) 
   
  if (isCount == 1):
    count_dict['call_count'] += len(cm_list) #count call without pre-complier headfile call
  return count_dict
    
def processFuncDecl(fp, outFname, sline,count_dict):
  ext0 = EXT0
  startLineNo = count_dict['lineNo']
  # get function name,filename and start-end lineno as follows
  nodeNo,tree_type,fnName,tfnFileSno,tfnEno=sline.lstrip().split()   
  fnFileSno=tfnFileSno[len(SOURCE_PATH0)+1:]
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
      sline=fp.readline(); count_dict['lineNo'] += 1  # skip identifier_node
      sline=fp.readline(); count_dict['lineNo'] += 1            
      tfnPara.append(' ')  #add new para to save real value
      while sline and ("parm_decl" not in sline and "bind_expr" not in sline):           
        tstr=''
        for s in sline.lstrip().split()[2:]: #change para value
          tstr += s +' ' 
        tfnPara[-1] = tstr.strip() +' '+tfnPara[-1]          
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
  call_list = []
  macro_list = []
  file_list = []
  while sline and (sline[0] == ' ' or sline[0] == '\t') and ("function_decl" not in sline):         
    # get Macro Expansion Info    
    if ("_expr" in sline):      
      if (sline.lstrip().split()[-1] != '()'):
        tlist=sline.lstrip().split()
        mlist_sline = fnName+': '+tlist[-2]+' '+tlist[-1][:-1][len(SOURCE_PATH0)+1:]
        if mlist_sline not in macro_list:        	
          macro_list.append(mlist_sline) 
        tmfloc = tlist[-3].split('(')[-1].split(':')[:-1]
        mfloc = tlist[-2]+' '+tmfloc[0][len(SOURCE_PATH0)+1:]+':'+tmfloc[-1]
        if mfloc not in file_list:        	
          file_list.append(mfloc)                 
    if ("call_expr" in sline): # find call location    
      sline_list = sline.lstrip().split()
      fcLoc = sline_list[2]
      while sline and ("identifier_node" not in sline): 
         sline=fp.readline();count_dict['lineNo'] += 1 #skip lines      
      nodeNo,tree_type,fcName=sline.lstrip().split()      
      tempstr=fnName+': '+fcName+' '+fcLoc[len(SOURCE_PATH0)+1:]
      if tempstr not in call_list:
        call_list.append(tempstr)      
    sline=fp.readline();count_dict['lineNo'] += 1

  # print function declation info 
  flag = 1;isCount = 0;
  for mlist in macro_list:
     if(mlist.find(fnFileSno) != -1):
       flag = 0;
       break;
  if (flag == 1):
    #count_dict['fndl_count'] += 1
    print >> outFname,'{} {} ({}) {} {} {}'.format(fnType,fnName,fnPara,fnFileSno,fnEno,startLineNo)
    fnFile=fnFileSno.split(':')[0]
    if (fnFile.endswith(fp.name[:-len(ext0)])):
      isCount = 1
      fcopath=os.path.dirname(outFname.name)+'/func_list.txt' 
      count_dict['fndl_count'] += 1
      with open(fcopath, 'a') as out:
         print >> out,'{}'.format(fnName) 
  # print call info
  count_dict=printToFile(outFname,count_dict,call_list,macro_list,file_list,isCount)                
  
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
    
    targetPath = os.path.dirname(outFname.name)
    count_dict=delSelfFuncCall(targetPath,count_dict)	##del self-func call 
    fnCall_dict=getFuncCallDict(targetPath,path)
    
    tempFile = targetPath + '/temp.txt'
    with open(tempFile,'w') as out:
		  for fnName,fcName_dict in  fnCall_dict.items():
		    print >> out,fnName
		    for fcName,fcLoc_list in fcName_dict.items():
		      print >> out,'  '+fcName
		      for fcLoc in fcLoc_list:
		        print >> out,'    '+fcLoc
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
    print "\ncollect interface info from file-->",os.getcwd()+'/'+V0_CODE
    V0_MANIFEST = V0_MANIFEST[:-len(ext0)]+ext2 
    with open(V0_MANIFEST, 'w') as outFname: #outFname is filename to save func interface
      collectIntFmfile(V0_CODE,outFname)   
    print 'Done.\n'  
  elif os.path.isdir(V0_CODE):
    print "\ncollect interface info from path-->",os.getcwd()+'/'+V0_CODE        
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
    print 'Done.\n' 
  
def task_collect():
    ext0=EXT0
    ext2=EXT2
    
    S0=sys.argv[1]
    
    global V0_CODE,V0_MANIFEST    
    V0_CODE=S0
    # path to solve
    if (os.path.exists('target') == False) or (os.path.isdir('target') == False):
        os.mkdir("target")
    V0_MANIFEST = 'target/'   
    print "\ntarget path to save info-->",os.getcwd()+'/'+V0_MANIFEST
    # call function to collect interface infomattion
    if os.path.exists(V0_CODE):
        if os.path.isfile(V0_MANIFEST+'func_list.txt'): # if file exist then del
            os.remove(V0_MANIFEST+'func_list.txt') 
        if os.path.isfile(V0_MANIFEST+'macro_list.txt'): # if file exist then del
            os.remove(V0_MANIFEST+'macro_list.txt')
        if os.path.isfile(V0_MANIFEST+'call_list.txt'): # if file exist then del
            os.remove(V0_MANIFEST+'call_list.txt')
        if os.path.isfile(V0_MANIFEST+'cm_list.txt'): # if file exist then del
            os.remove(V0_MANIFEST+'cm_list.txt')
        if os.path.isfile(V0_MANIFEST+'file_list.txt'): # if file exist then del
            os.remove(V0_MANIFEST+'file_list.txt')
        if os.path.isfile(V0_MANIFEST+'func_list.txt'): # if file exist then del
            os.remove(V0_MANIFEST+'func_list.txt')
        collectInt(V0_CODE,V0_MANIFEST)       
    else:
        print "cannot find path or file",V0_CODE
 
def main():
    task_collect()
  
if __name__ == '__main__':
    main()
