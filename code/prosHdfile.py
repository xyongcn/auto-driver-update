#!/usr/bin/python
# python file to get headfile function propertype 

import os
import sys
from subprocess import check_output
from collections import OrderedDict

SOURCE_PATH0 = '/home/ryyan/SOURCE/linux-3.5.4/'
SOURCE_PATH1 = '/home/ryyan/SOURCE/linux-3.8.13/'
TARGET_PATH = 'target/'
#FILE_TO_INPUT = 'source/console/vgacon.c'
CTAGSFILE_EXT = '_ctags.txt'

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
  
  ctags_dict = OrderedDict()
  with open(filename) as fp:
    sline = fp.readline()
    while sline:
      if (sline !='\n' ):
        tlist = sline.split()
        name = tlist[0]
        _type = tlist[1]
        rows = tlist[2]
        _file = tlist[3][len(SOURCE_PATH):]
        state_list = tlist[4:]
        if (cmp(_type,'macro')==0 or cmp(_type,'prototype')==0 or cmp(_type,'function')==0):
          statement = ' '.join(state_list)
          fileph = tlist[3]
          while statement.endswith(','):
            rows = int(rows) + 1
            temp=check_output(['sed','-n',str(rows)+'p',fileph]).strip()
            statement = statement + temp
          tstr =' '+ _type+'  '+_file+'  '+str(rows)+'  '+statement
          ctags_dict[name] = tstr
      sline = fp.readline()
  printDictMethod(ctags_dict,filename)
  print filename,'file is revised successful!'
  #return ctags_dict
  
def getCtagsFile(hdFileTxt,vers):
  outCtagsPath = TARGET_PATH+'v'+vers+CTAGSFILE_EXT
  SOURCE_PATH = getSrcPath(vers)
  assert os.path.isfile(hdFileTxt),'input file '+hdFileTxt+' not found!\n'
  
  with open(outCtagsPath,'w') as out:
    with open(hdFileTxt) as fp:
      hdFileName = fp.readline();
      while hdFileName:
        filepath1 = SOURCE_PATH+'include/'+hdFileName[:-1]
        filepath2 = SOURCE_PATH+'arch/x86/include/'+hdFileName[:-1]
        if os.path.isfile(filepath1):
          filepath = filepath1
        else:
          filepath = filepath2
        assert os.path.isfile(filepath),'file '+filepath+' not found!\n'
        cmd_string = ['ctags','-xu','--c-kinds=+p',filepath] #,'--extra=+q','--totals'
        hdFnd_list = check_output(cmd_string).rstrip('\0').split('\0')
        for hflist in hdFnd_list:
          print >> out,hflist
        hdFileName = fp.readline()
  print outCtagsPath,'file is generated successful!'
  
def main():
    print '\npython file:',sys.argv[0],'running...'
    print 'input file:',sys.argv[1]
    hdFileTxt = sys.argv[1]
    getCtagsFile(hdFileTxt,'0')
    reviseCtagsFile('0')
    getCtagsFile(hdFileTxt,'1')
    reviseCtagsFile('1')
    print 'Done'
  
if __name__ == '__main__':
    main()
