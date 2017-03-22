# -*- coding: UTF-8 -*-

'''
 To get interface infomation
'''

import os
import sys
from subprocess import check_output

EXT0 = '.ind' # AST file
EXT2 = '.int' #interface file

def processFuncDecl(fp, outFname, sline,count_dict):
  ext0 = EXT0
  startLineNo = count_dict['lineNo']
  # get function name,filename and start-end lineno as follows
  nodeNo,tree_type,fnName,tfnFile,tfnSEno=sline.lstrip().split()   
  fnFile=tfnFile.split(':')[0]
  fnSEno=tfnFile.split(':')[1]+":"+tfnFile.split(':')[2]
  fnSEno=fnSEno+" "+tfnSEno.split(':')[1]+":"+tfnSEno.split(':')[2]
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
                    
  # print function declation info as follows
  print >> outFname,'{} {} ({}) {} {} {}'.format(fnType,fnName,fnPara,fnFile,fnSEno,startLineNo)
  
  # get function call info as follows
  call_lists = []
  macro_lists = []
  while sline and (sline[0] == ' ' or sline[0] == '\t') and ("function_decl" not in sline):         
    # get Macro Expansion Info    
    if (("bind_expr" in sline) or ("nop_expr" in sline)):      
      if (sline.lstrip().split()[-1] != '()'):
        list_sline = sline.lstrip().split()[-2]+' '+sline.lstrip().split()[-1][:-1]        
        if list_sline not in macro_lists:        	
          macro_lists.append(list_sline)      
    
    if ("call_expr" in sline): # find call location    
      #slen = len(sline) - len(sline.lstrip()) # indent len of call_expr line   
      sline_list = sline.lstrip().split()
      fcLoc = sline_list[2]
      #eflg =sline_list[3]
      while sline and ("identifier_node" not in sline): 
         sline=fp.readline();count_dict['lineNo'] += 1 #skip lines      
      nodeNo,tree_type,fcName=sline.lstrip().split()      
      call_lists.append(fcName+' '+fcLoc)    
  
    sline=fp.readline();count_dict['lineNo'] += 1
  '''
  count_dict['call_count'] += len(call_lists)
  print >> outFname,'func_call: {}'.format(len(call_lists))
  for clist in call_lists:
    print >> outFname,'  {}: {}'.format(fnName,clist)
  ''' 
  if (fnFile.endswith(fp.name[:-len(ext0)])):     
    sopath = outFname.name+'s'
    with open(sopath, 'a') as out:
      print >> out,'{} {} ({}) {} {} {}'.format(fnType,fnName,fnPara,fnFile,fnSEno,startLineNo)       
    
    copath = outFname.name+'c'    
    with open(copath, 'a') as out:
      #print >> out,'func_call: {}'.format(len(call_lists))
      for clist in call_lists:
        print >> out,'{}: {}'.format(fnName,clist)
      #print >> out,'macro_info: {}'.format(len(macro_lists))
      for mlist in macro_lists:
        tmlist=mlist.split()
        print >> out,'{}: {} {}'.format(fnName,tmlist[-2],tmlist[-1])
    
    bopath=os.path.dirname(outFname.name)+'/cm.txt'
    with open(bopath, 'a') as out:
      if len(call_lists) > 0:
        print >> out,'===================call_list======================'
        for clist in call_lists:
          print >> out,clist            
      if len(macro_lists) > 0:
        print >> out,'===================macro_lists===================='
        for mlist in macro_lists:
          print >> out,mlist       
        
  count_dict['call_count'] += len(call_lists) + len(macro_lists)
  fp.seek(-len(sline),1); count_dict['lineNo'] -= 1 #back to last line
  return count_dict
  
def collectIntFmfile(path,outFname):
    count_dict={'fndl_count':0,'lineNo':0,'call_count':0}
    with open(path) as fp:
      sline=fp.readline();count_dict['lineNo'] += 1
      while sline:        
        if ((sline[0] != ' ' and sline[0] != '\t') and ("function_decl" in sline)):
          count_dict=processFuncDecl(fp, outFname, sline,count_dict)
          count_dict['fndl_count'] += 1
        sline=fp.readline();count_dict['lineNo'] += 1
      else:
        count_dict['lineNo'] -= 1
    print path,'-->\n\ttotal line',count_dict['lineNo'],'\n\ttotal function decl',count_dict['fndl_count'],'\n\ttotal function call',count_dict['call_count']
    return count_dict['fndl_count']

def collectInt(prefix,outDir):
  ext0=EXT0
  ext2=EXT2
  
  global V0_MANIFEST
  V0_MANIFEST = outDir+'V-'+os.path.split(prefix.strip('/'))[-1]
  
  if os.path.isfile(V0_CODE):
    assert V0_CODE.endswith(ext0),'file not found with ext *.'+ext0
    print "\ncollect interface info from file-->",os.getcwd()+'/'+V0_CODE
    V0_MANIFEST = V0_MANIFEST[:-len(ext0)]+ext2 
    with open(V0_MANIFEST, 'w') as outFname: #outFname is filename to save func interface
      sopath = outFname.name+'s'
      if os.path.isfile(sopath): # if file exist then del
        os.remove(sopath)
      copath = outFname.name+'c'
      if os.path.isfile(copath): # if file exist then del
        os.remove(copath)
        
      collectIntFmfile(V0_CODE,outFname)
    print 'Done.\n'  
  elif os.path.isdir(V0_CODE):
    print "\ncollect interface info from path-->",os.getcwd()+'/'+V0_CODE        
    V0_MANIFEST = V0_MANIFEST+ext2 
    with open(V0_MANIFEST, 'w') as outFname: #outFname is filename to save func interface
      opath = outFname.name+'s'
      if os.path.isfile(opath): # if file exist then del
        os.remove(opath)
      copath = outFname.name+'c'
      if os.path.isfile(copath): # if file exist then del
        os.remove(copath)
        
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
        collectInt(V0_CODE,V0_MANIFEST)         
    else:
        print "cannot find path or file",V0_CODE
  


def main():
    task_collect()
  
if __name__ == '__main__':
    main()
