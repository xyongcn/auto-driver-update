#!/usr/bin/python
# python file to test
# -*- coding: UTF-8 -*-

import os
import commands
from subprocess import check_output
from Tkinter import *
import ttk #Combobox
import tkMessageBox
import linecache #file cache

ROOTDIR = os.environ['HOME']+"/myProjects"
AIDLOG_FILE_SUFFIX = "assitLog.txt"
AIDLOGDIR = "assitLog/"


class ResutShow:
	#init data,draw frame
	def __init__(self):#
		
		#window set
		window = Tk();
		window.title("DDAU Result Show")
		window.update()
		window.maxsize(1000,980)
		window.minsize(660,400)
		scnWidth = window.winfo_reqwidth()
		scnHeight = window.winfo_height()
		width,height = window.minsize() #current width,height
		size = '%dx%d+%d+%d'%(width,height,(scnWidth-360)/2,(scnHeight-300)/2)
		window.geometry(size)
		
		#top Label
		Label(window, text="DDAU Result Show".decode('gbk').encode('utf8'), font=('Arial', 18)).pack()
		#center frame
		frame = Frame(window)
		frame.pack()
		#bottom Listbox
		self.var_L = StringVar()
		self.listbox = Listbox(window,listvariable=self.var_L,font =('Arial',14)) 
		self.listbox.pack(side=TOP, fill=BOTH, expand=1)
		self.scbar = Scrollbar(window,orient='horizontal',command=self.listbox.xview)
		self.scbar.pack(side=BOTTOM,fill=BOTH)
		self.scbar.configure(bg='#eeeeff')
		self.listbox['xscrollcommand'] = self.scbar.set
		
		#show frame
		frame_T = Frame(frame)
		frame_T.pack();
		label = Label(frame_T, text="* Drivers Assit File Select:".decode('gbk').encode('utf8'), font=('Arial', 12))
		#  get Assit File List
		self.path_list = self.getFileList()
		#  smplify Assit File List
		self.plist_show = self.simplifyPathList(self.path_list)
		
		self.str1 = StringVar()
		self.plistChosen = ttk.Combobox(frame_T, textvariable = self.str1,values=self.plist_show)
		self.plistChosen.current(0)
		self.plistChosen.config(state='readonly',foreground='#0000ee')
		self.plistChosen.bind("<<ComboboxSelected>>", self.show_change)
		label.grid(row = 1, column = 1, rowspan = 2, pady = 2)
		self.plistChosen.grid(row = 1, column = 2, rowspan = 2, padx = 4, pady = 2)
		
		#menu frame
		frame_B = Frame(frame)
		frame_B.pack();
		self.v1 = IntVar()
		self.Aradiobtn = Radiobutton(frame_B, text = "A-level ", bg = "#ee0000", variable = self.v1, value = 1, command = self.processRaidobutton)
		self.Bradiobtn = Radiobutton(frame_B, text = "B-level ", bg = "#eeee00", variable = self.v1, value = 2, command = self.processRaidobutton)
		self.Cradiobtn = Radiobutton(frame_B, text = "C-level ", bg = "#00ee00", variable = self.v1, value = 3, command = self.processRaidobutton)
		self.Tradiobtn = Radiobutton(frame_B,text = "All-level ",bg= "#aabb00",variable = self.v1,value = 4,command = self.processRaidobutton)
		self.btDesc = Button(frame_B, text="Descriptions", bg = "#aacccc")
		self.btDesc.bind("<Button-1>", self.printDesc)#bind event
		
		self.Aradiobtn.grid(row = 1,column = 1,rowspan = 2,padx = 4,pady = 5)
		self.Bradiobtn.grid(row = 1,column = 2,rowspan = 2,padx = 4,pady = 5)
		self.Cradiobtn.grid(row = 1,column = 3,rowspan = 2,padx = 4,pady = 5)
		self.Tradiobtn.grid(row = 1,column = 4,rowspan = 2,padx = 4,pady = 5)
		self.btDesc.grid(row = 1,column = 5,rowspan = 2,padx = 4,pady = 5)
		
		#load Descriptions
		self.showDesc() 
	
	def show_change(self,event):
		self.v1.set(4) == 1
		self.processRaidobutton()
		
	def processRaidobutton(self):
		self.listbox.delete(0, END)
		index = self.plistChosen.current()
		fileph = self.path_list[index]
		
		if os.path.isfile(fileph): 
			aret,bret,cret=self.getFileLineNo(fileph)
			fileCacheList = linecache.getlines(fileph)
		else:
			tkmbtitle = "Message Notification"
			tkmbcontent = "batch_run.sh mush be first executed!"
			tkMessageBox.showinfo(tkmbtitle, tkmbcontent)
			self.showFNFError(fileph)
			return
		
		if self.v1.get() == 1:
			if aret[0] == 0 and bret[0] == 0:
				Aloc = int(aret[1].split(':')[0])-1
				Bloc = int(bret[1].split(':')[0])
				ablist = fileCacheList[Aloc:Bloc-1]
				self.printListToTextbox(ablist)
			else:
			  self.printUNError()
			  
		elif self.v1.get() == 2:
			if bret[0] == 0 and cret[0] == 0:
				Bloc = int(bret[1].split(':')[0])-1
				Cloc = int(cret[1].split(':')[0])
				bclist = fileCacheList[Bloc:Cloc-1]
				self.printListToTextbox(bclist)
			else:
			  self.printUNError()
		
		elif self.v1.get() == 3:
			if cret[0] == 0 :
				Cloc = int(cret[1].split(':')[0])-1
				clist = fileCacheList[Cloc:]
				self.printListToTextbox(clist)
			else:
			  self.printUNError()
		
		else:
			self.printListToTextbox(fileCacheList)
	
	def getFileLineNo(self,fileph):
		cmds = "grep -nw "
		Aflag = "= A  level ="
		Bflag = "= B  level ="
		Cflag = "= C  level ="
		cmd_string = cmds+" '"+Aflag+"' "+fileph
		aret=commands.getstatusoutput(cmd_string)
		cmd_string = cmds+" '"+Bflag+"' "+fileph
		bret=commands.getstatusoutput(cmd_string)
		cmd_string = cmds+" '"+Cflag+"' "+fileph
		cret=commands.getstatusoutput(cmd_string)
		return aret,bret,cret
	
	def printListToTextbox(self, textlist):
		self.listbox.delete(0, END)
		lineno = 1
		for vlist in textlist:
			vlist = vlist.rstrip('\n')
			self.listbox.insert(END, str(lineno)+'  ' +vlist)
			lineno = lineno + 1
	
	def printUNError(self):
		self.listbox.insert(END, "Unexpected Error Occurred:")
		self.listbox.insert(END, "  Please try again.")
		self.listbox.insert(END, "  Please make sure these info in current file:")
		self.listbox.insert(END, "    = A  level =")
		self.listbox.insert(END, "    = B  level =")
		self.listbox.insert(END, "    = C  level =")
		tkmbtitle = "UnexpectedError"
		tkmbcontent = "Unexpected Error Occurred, try again!"
		tkMessageBox.showwarning(tkmbtitle, tkmbcontent)
	
	def simplifyPathList(self, path_list):
		#simplify path List
		plist_show = []
		for vlist in path_list: #enumerate()
			plist_show.append(os.path.basename(vlist)) 
		return plist_show
	
	def getFileList(self):
		rootDir = ROOTDIR
		if not rootDir.endswith('/'):
			rootDir = rootDir + '/'
		filepath = rootDir + AIDLOGDIR
		file_suffix = AIDLOG_FILE_SUFFIX
		path_list = check_output(['find',filepath,'-name','*'+file_suffix,'-print0']).rstrip('\0').split('\0')
		path_list.sort()
		return path_list
	
	def printDesc(self, event): 
		self.showDesc()
		self.getFileList()

	def showDesc(self): 
		self.listbox.delete(0, END)
		rootDir = ROOTDIR
		if not rootDir.endswith('/'):
			rootDir = rootDir + '/'
		filename = rootDir+'assitlog_description.txt'
		
		if os.path.isfile(filename):
			with open(filename) as fp:
				sline=fp.readline().rstrip('\n')
				while sline:
					sline = sline.strip('\n')
					self.listbox.insert(END, sline)
					sline=fp.readline()
		else:
			self.showFNFError(filename)

	def showFNFError(self,filename):
		self.listbox.insert(END, "FileNotFoundError:")
		self.listbox.insert(END, "    file "+filename+" not found!")
		self.listbox.insert(END, "    file "+filename+" Loading error!")
		self.listbox.insert(END, "    Please make sure file "+filename+" exists.")
		tkMessageBox.showerror("FileNotFoundError",filename+" file not found!")

def ResutDisplay():
	ResutShow()
	mainloop()

def main():
	ResutDisplay()

if __name__ == '__main__':
	main()
	
