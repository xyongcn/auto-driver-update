#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LEN 1024

char filepath1[10] = "include/";
char filepath2[20] = "arch/x86/include/";
char filepath3[30] = "arch/x86/include/uapi/";
char *srcPath = NULL;

int getHeaderFile(char sFileName[],char outHeadFname[]);

int get2ndHdFile(char codePath[],char outHeadFname[],char outFname[])
{
	FILE *fpIn = NULL;
	FILE *fpOut = NULL;
	char sline[120];
	char sHeadFile[400][120];
	char sHdFileList[400][120];
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
	int sum=count;
	char tempFname[30] = "target/tmphfile.txt";
	for(i=0;i<count;i++)
	{
		memset(filepath,0,sizeof(filepath));
		sprintf(filepath,"%s%s%s%s",srcPath,codePath,filepath1,sHeadFile[i]);
		if((fpIn=fopen(filepath, "r"))==NULL)
		  sprintf(filepath,"%s%s%s%s",srcPath,codePath,filepath2,sHeadFile[i]);
		if((fpIn=fopen(filepath, "r"))==NULL)
		  sprintf(filepath,"%s%s%s%s",srcPath,codePath,filepath3,sHeadFile[i]);
		
		int ret = getHeaderFile(filepath,tempFname);//call functions
		if( (ret==0) && (fpIn=fopen(tempFname, "r")) )
		{
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
	}
	//get 3nd header file
	int total=sum;
	for(i=count;i<sum;i++)
	{
		memset(filepath,0,sizeof(filepath));
		sprintf(filepath,"%s%s%s%s",srcPath,codePath,filepath1,sHdFileList[i]);
		if((fpIn=fopen(filepath, "r"))==NULL)
		  sprintf(filepath,"%s%s%s%s",srcPath,codePath,filepath2,sHdFileList[i]);
		if((fpIn=fopen(filepath, "r"))==NULL)
		  sprintf(filepath,"%s%s%s%s",srcPath,codePath,filepath3,sHeadFile[i]);
		
		int ret = getHeaderFile(filepath,tempFname);//call functions
		if( (ret==0) && (fpIn=fopen(tempFname, "r")) )
		{
			while ((fgets(sline,MAX_LEN,fpIn)!=NULL)&&(!feof(fpIn)))
			{
				len = strlen(sline);
	 			sline[len-1] = '\0';
				int j=0;
				for(j=0;j<total;j++)
				{// delDuplicateLine
					if(strcmp(sHdFileList[j],sline) == 0)
					  break;
				}
				char *p=strstr(sline,"/");
				if((p!=NULL) && (j>=total)){
					strcpy(sHdFileList[total],sline);
					total++;
				}
			}
			fclose(fpIn);
		}
	}
	printf("%s total header file-->%d\n",outFname,total);
	if(remove(tempFname)== 0)
     printf("Removed temp file %s.\n", tempFname);
  else
     printf("Removed temp file %s failed.\n", tempFname);
	
	fpOut = fopen(outFname, "w");
	for(i=0;i<total;i++)
	  fprintf(fpOut, "%s\n", sHdFileList[i]);
	fclose(fpOut);  
	return 0;
}



