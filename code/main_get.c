#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char codePath1[30] = "/SOURCE/linux-3.5.4/";
char codePath2[30] = "/SOURCE/linux-3.8.13/";
char outHeadFname[30] = "target/headfile.txt";
char outFname1[30] = "target/v0_headfile.txt";
char outFname2[30] = "target/v1_headfile.txt";
	
int LinePreprocessing(FILE *fpIn, char *sReadLine, long *zLineNo);
int getHeaderFile(char sFileName[],char outHeadFname[]);
int get2ndHdFile(char codePath[],char outHeadFname[],char outFname[]);

int main(int argc, char *argv[])
{
	char sFileName[160];
	int ret=0,ret2=0;
	
	if(argc <= 1){
	  printf("please input file name：\n");
	  scanf("%s", sFileName);
	}
	
	sprintf(sFileName,"%s",argv[1]);
	printf("program getHeaderFile running ....\n");	
	ret=getHeaderFile(sFileName,outHeadFname);	
	if(ret==0)
		printf("getHeaderFile running successful.\n");
	else{
		printf("getHeaderFile running faild.\n");
		exit(1);
	}
	
	printf("program get2ndHdFile running ....\n");	
	ret=get2ndHdFile(codePath1,outHeadFname,outFname1);
	ret2=get2ndHdFile(codePath2,outHeadFname,outFname2);	
	if(ret==0 && ret2 ==0)// 
	{
		printf("get2ndHdFile running successful.\n");
		printf("generated file %s.\ngenerated file %s.\n",outFname1,outFname2);
	}else{
		printf("get2ndHdFile running faild.\n");
		exit(1);
	}

}
