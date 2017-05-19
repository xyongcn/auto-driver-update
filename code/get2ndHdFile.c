#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LEN 1024

char filepath1[10] = "include/";
char filepath2[20] = "arch/x86/include/";
char *srcPath = NULL;

int getHeaderFile(char sFileName[],char outHeadFname[]);

int get2ndHdFile(char codePath[],char outHeadFname[],char outFname[])
{
	FILE *fpIn = NULL;
	FILE *fpOut = NULL;
	char sline[50];
	char sHeadFile[50][50];
	char sHdFilePath[300][100];
	char sHdFileList[300][50];
	char filepath[120];
	int len = 0;

	int count=0;
	if(fpIn=fopen(outHeadFname, "r"))
	{	
	  while ((fgets(sline,MAX_LEN,fpIn)!=NULL)&&(!feof(fpIn))) //按行进行处理
		{
		  len = strlen(sline);
 			sline[len-1] = '\0';
		  strcpy(sHeadFile[count],sline);
		  strcpy(sHdFileList[count],sline);
		  count++;
	  }
	  fclose(fpIn); 
	}
	else
	{
		printf("cannot open header file ：%s\n", outHeadFname);
		exit(1);
	}
	
	srcPath = getenv("HOME"); // get home path
	int i=0;
	for(i=0;i<count;i++)
	{
		memset(filepath,0,sizeof(filepath));
		sprintf(filepath,"%s%s%s%s",srcPath,codePath,filepath1,sHeadFile[i]);
		if(fpIn=fopen(filepath, "r"))
		{
		  strcpy(sHdFilePath[i],filepath);
		  fclose(fpIn);
		}
		else
		{
		  sprintf(filepath,"%s%s%s%s",srcPath,codePath,filepath2,sHeadFile[i]);
		  strcpy(sHdFilePath[i],filepath);
		}
	}
	
	int sum=count;
	char tempFname[30] = "target/tmphfileList.txt";
	for(i=0;i<count;i++)
	{
		getHeaderFile(sHdFilePath[i],tempFname);//call functions
		fpIn=fopen(tempFname, "r");
	  while ((fgets(sline,MAX_LEN,fpIn)!=NULL)&&(!feof(fpIn)))
		{
		  len = strlen(sline);
 			sline[len-1] = '\0';
		  int j=0;
		  for(j=0;j<sum;j++)
		  {// delDuplicateLine
		  	if(strcmp(sHdFileList[j],sline) == 0)
		  	  break;
		  }
		  char *p=strstr(sline,"/");
		  if((p!=NULL) && (j>=sum)){
		  	strcpy(sHdFileList[sum],sline);
		  	sum++;
		  }
	  }
		fclose(fpIn);
	}
	if(remove(tempFname) == 0 )
     printf("Removed temp file %s.\n", tempFname);
  else
     printf("Removed temp file %s failed.\n", tempFname);
	
	fpOut = fopen(outFname, "w");
	for(i=0;i<sum;i++)
	  fprintf(fpOut, "%s\n", sHdFileList[i]);
	fclose(fpOut);  
	return 0;
}



