#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int LinePreprocessing(FILE *fpIn, char *sReadLine, long *zLineNo);
int getHeaderFile(char sFileName[]);
int getFunCall(char sFileName[]);

int main(int argc, char *argv[])
{
	char sFileName[60];
	int ret=0;
	
	if(argc <= 1){
	  printf("please input file name：\n");
	  scanf("%s", sFileName);
	}
	sprintf(sFileName,"%s",argv[1]);
	printf("program getHeaderFile running ....\n");	
	ret=getHeaderFile(sFileName);	
	if(ret==0)
		printf("getHeaderFile running successful.\n");
	else{
		printf("getHeaderFile running faild.\n");
		exit(1);
	}	
	printf("program getFunCall running ....\n");	
	ret=getFunCall(sFileName);	
	if(ret==0)
		printf("getFunCall running successful.\n");
	else
		printf("getFunCall running faild.\n");
	return 0;
}
