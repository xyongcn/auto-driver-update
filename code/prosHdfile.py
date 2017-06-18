#!/usr/bin/python
# python file to get headfile function propertype 

import os
import sys
from subprocess import check_output
from collections import OrderedDict

SOURCE_PATH0 = os.environ['HOME']+'/SOURCE/linux-3.5.4/'
SOURCE_PATH1 = os.environ['HOME']+'/SOURCE/linux-3.8.13/'
TARGET_PATH = 'target/'
CURRENT_PATH = os.getcwd()
CTAGSFILE_EXT = '_ctags.txt'
HEADERFILE_EXT = '_headfile.txt'

def printDictMethod(dictname,filename):
  with open(filename,'w') as out:
    for (k,v) in dictname.items():
      print >> out,k,v

def getSrcPath(vers):  
  if (cmp(vers,'0') == 0):
    return SOURCE_PATH0
  else:
    return SOURCE_PATH1

def reviseCtagsFile(vers):
  filename = TARGET_PATH+'v'+vers+CTAGSFILE_EXT
  SOURCE_PATH = getSrcPath(vers)
  print filename,'file is reviseding ...'
  
  ctags_dict = OrderedDict()
  with open(filename) as fp:
    sline = fp.readline()
    while sline:
      if (sline !='\n' ):
        tlist = sline.split()
        name = tlist[0]
        _type = tlist[1]
        rows = tlist[2];rowstart = rows
        _file = tlist[3][len(SOURCE_PATH):]
        state_list = tlist[4:]
        if len(state_list)==0:
          print 'state_list==0',sline
          break
        fileph = tlist[3]
        if _type in ('macro','function','prototype'):
          statement = state_list[0]
          for slt in state_list[1:]:	#handle more space
            if statement.endswith(','):
              statement = statement + slt
            else:
              statement = statement +' '+ slt
          statement = statement.split('/*')[0].strip() #del notes
          while statement.endswith(','):
            rows = int(rows) + 1
            temp=check_output(['sed','-n',str(rows)+'p',fileph]).strip()
            statement = statement + temp
          while(statement.endswith('\\')):
            rows = int(rows) + 1
            temp=check_output(['sed','-n',str(rows)+'p',fileph]).strip()
            statement = statement.rstrip('\\').rstrip()+' '+ temp
          ctags_dict[name] = ' '+ _type+'  '+_file+'  '+rowstart+'  '+statement
        
        elif _type in ('struct','enum','union'):
          statement = ' '.join(state_list).split('/*')[0].strip()
          statement = statement.split('/*')[0].strip() #del notes
          aliasname_list = []
          if not statement.endswith(';'): # not one decl
		        openbrace_unmatch = 0	# open brace-->{ , close brace-->}
		        openbrace_unmatch += statement.count('{')
		        temp_dict = {}
		        rowend = int(rows) + 1
		        temp=check_output(['sed','-n',str(rowend)+'p',fileph]).strip()
		        while True:  # find end rows of struct
		          openbrace_unmatch += temp.count('{')
		          openbrace_unmatch -= temp.count('}')
		          if openbrace_unmatch == 0:
		            break
		          rowend = int(rowend) + 1 # refresh end rows of struct
		          if('{' in temp and len(temp) > 1 and '*' not in temp): # recored unamed/named struct member start flag
		            temp_dict[rowend] = temp.split('/*')[0].strip()
		          if temp.startswith('}') and temp.endswith(';'): # recored named struct member end flag
		            temp_dict[rowend] = temp.split('/*')[0].strip()
		          temp=check_output(['sed','-n',str(rowend)+'p',fileph]).strip()
		        endstmt = temp.split('/*')[0].strip() # end flag of struct
		        
		        #get alias name of data struct 
		        if not endstmt.endswith('};'):
		          i = 0;
		          for cstr in endstmt[::-1]:
		            if cstr == '}':
		              break
		            i += 1
		          aliasname = endstmt[(len(endstmt)-i):-1].strip()
		          if '(' not in aliasname:
		            aliasname_list = aliasname.split(',')
		        
		        if '{' not in statement:
		          statement = statement + ' {'
		        sline2 = fp.readline()
		        while sline2 and (sline2 != '\n'):
		          rows = sline2.split()[2]
		          if int(rows) > int(rowend):
		            break
		          state_list2 = sline2.split()[4:]
		          statement2 = ' '.join(state_list2).split('/*')[0].strip()
		          if int(rows) in temp_dict: #mod struct member struct/union/enum start and end
		            if not statement.endswith(temp_dict[int(rows)]):
		              statement = statement +' '+ temp_dict[int(rows)] 
		          while statement2.endswith(',') and ('member' in sline2):  #enumerator endswith ',' so exclude it
		          	rows = int(rows) + 1
		          	temp=check_output(['sed','-n',str(rows)+'p',fileph]).split('/*')[0].strip()
		          	statement2 = statement2 + temp
		          
		          if not statement.endswith(statement2):
		            statement = statement +' '+ statement2  # merge statement
		          sline2 = fp.readline() # read next line
		        if not statement.endswith(endstmt):
		          statement = statement +' '+ endstmt 
		        fp.seek(-len(sline2),1); #back to last line    
          else:
            if not statement.endswith('};'):
              i = 0;
              for cstr in statement[::-1]:
                if cstr == '}':
                  break
                i += 1
            aliasname = statement[(len(statement)-i):-1].strip()
            if '(' not in aliasname:
              aliasname_list = aliasname.split(',')
          
          ctags_dict[name] = ' '+ _type+'  '+_file+'  '+rowstart+'  '+statement
          if len(aliasname_list)>0:
            for vname in aliasname_list:
              ctags_dict[vname] = ' '+ _type+'  '+_file+'  '+rowstart+'  '+statement
        elif _type in ('member','enumerator'): #typedef struct,typedef enum,struct class
          statement = ' '.join(state_list).split('/*')[0].strip()
          statement = statement.split('/*')[0].strip() #del notes
          namelist = []
          temp = statement
          while True: # find start rows of data type
            if '{' in temp: 
              if ('struct' not in temp) and ('enum' not in temp) and ('union' not in temp):
                rowstart = int(rowstart) - 1
                temp=check_output(['sed','-n',str(rowstart)+'p',fileph]).split('/*')[0].strip() 
              break
            rowstart = int(rowstart) - 1
            temp=check_output(['sed','-n',str(rowstart)+'p',fileph]).split('/*')[0].strip()  
          startstmt = temp.split('/*')[0].strip() # start flag
          
          rowend = rowstart
          if not startstmt.endswith(';'):
            openbrace_unmatch = 0
            openbrace_unmatch += startstmt.count('{')
            rowend = rowend + 1
            temp=check_output(['sed','-n',str(rowend)+'p',fileph]).strip()
            while True:  # find end
              openbrace_unmatch += temp.count('{')
              openbrace_unmatch -= temp.count('}')
              if openbrace_unmatch == 0:
                break
              rowend = rowend + 1
              temp=check_output(['sed','-n',str(rowend)+'p',fileph]).strip()
            endstmt = temp.split('/*')[0].strip() # end flag
            
            if not ('typedef' in startstmt):
              _type = startstmt.split()[0]
            else:
              _type = startstmt.split()[1]
            
            if not endstmt.endswith('};'):
              #name = endstmt[1:-1].strip()
              i = 0;
              for cstr in endstmt[::-1]:
                if cstr == '}':
                  break
                i += 1
              name = endstmt[(len(endstmt)-i):-1].strip()
              if '(' not in name:
                namelist = name.split(',')
            else:
              name = 'unamed-'+_type
            
            if '{' not in startstmt:
              startstmt = startstmt + ' {'
            if int(rows) <= int(rowend):
              statement = startstmt +' '+ statement
            sline2 = fp.readline()
            while sline2 and (sline2 != '\n'):
              rows = sline2.split()[2]
              if int(rows) > int(rowend):
                break
              state_list2 = sline2.split()[4:]
              statement2 = ' '.join(state_list2).split('/*')[0].strip()
              while statement2.endswith(',') and ('member' in sline2):  #enumerator endswith ',' so exclude it
                rows = int(rows) + 1
                temp=check_output(['sed','-n',str(rows)+'p',fileph]).split('/*')[0].strip()
                statement2 = statement2 + temp
              if not statement.endswith(statement2):
                statement = statement +' '+ statement2  # merge statement
              sline2 = fp.readline() # read next line    
            if not statement.endswith(endstmt):
              statement = statement +' '+ endstmt
            fp.seek(-len(sline2),1); #back to last line  
          else:
            if 'struct' in statement:
              _type = 'struct'
            elif 'enum' in statement:
              _type = 'enum'
            elif 'union' in statement:
              _type = 'union'
            else:
              _type = 'typedef'
            
            if statement.endswith('};'):
              name = 'unamed-' +_type
            else:
              i = 0;
              for cstr in statement[::-1]:
                if cstr == '}':
                  break
                i += 1
              name = statement[(len(statement)-i):-1].strip()
              if '(' not in name:
                namelist = name.split(',')
          if 'unamed' not in name:
            for vname in namelist:
              ctags_dict[vname] = ' '+ _type+'  '+_file+'  '+str(rowstart)+'  '+statement
        else: #other typedef
          pass
      sline = fp.readline()# move file pointer
  printDictMethod(ctags_dict,filename)
  print filename,'file is revised successful!'
  #return ctags_dict

def getCtagsFile(vers):
  hdFileTxt = TARGET_PATH+'v'+vers+HEADERFILE_EXT
  outCtagsPath = TARGET_PATH+'v'+vers+CTAGSFILE_EXT
  SOURCE_PATH = getSrcPath(vers)
  assert os.path.isfile(hdFileTxt),'input file '+hdFileTxt+' not found!\n'
  
  with open(outCtagsPath,'w') as out:
    with open(hdFileTxt) as fp:
      hdFileName = fp.readline();
      while hdFileName:
        filepath1 = SOURCE_PATH+'include/'+hdFileName[:-1]
        filepath2 = SOURCE_PATH+'arch/x86/include/'+hdFileName[:-1]
        filepath3 = SOURCE_PATH+'include/uapi/'+hdFileName[:-1]
        filepath4 = SOURCE_PATH+'arch/x86/include/uapi/'+hdFileName[:-1]
        if os.path.isfile(filepath1):
          filepath = filepath1
        elif os.path.isfile(filepath2):
          filepath = filepath2
        elif os.path.isfile(filepath3):
          filepath = filepath3
        elif os.path.isfile(filepath4):
          filepath = filepath4
        else:
          filepath = ""
          print 'header file '+hdFileName[:-1]+' in',SOURCE_PATH,' not found!\n'
        if cmp(filepath,"")!= 0:
		      cmd_string = ['ctags','-xu','--c-kinds=+p',filepath] #,'--extra=+q'
		      hdFnd_list = check_output(cmd_string).rstrip('\0').split('\0')
		      for hflist in hdFnd_list:
		        print >> out,hflist
        hdFileName = fp.readline()
  print outCtagsPath,'file is generated successful!'

def main():
    print '\npython file:',sys.argv[0],'running...'
    getCtagsFile('0')
    getCtagsFile('1')
    reviseCtagsFile('0')
    reviseCtagsFile('1')
    print 'Done\n'
  
if __name__ == '__main__':
    main()
