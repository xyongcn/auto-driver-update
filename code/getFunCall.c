#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_LEN 1024

char outCflowFname[50] = "target/cflow_fc.txt";

int getFunCall(char sFileName[])
{	
	char outFileName[500]="";	
	int i=strlen(sFileName)-2;
	int k=0;
	
	while(i>0&&sFileName[i]!='.') i--;
	for(int j=0;j<i;j++){
		outFileName[k++]=sFileName[j];
	}
	sprintf(outFileName,"%s_fun.txt",outFileName); //get outFileName(function file name)
	char cmd_string[500]="cflow -r -d 2";
	sprintf(cmd_string,"%s %s > %s",cmd_string,sFileName,outFileName);
	
	system(cmd_string);

	char sReadLine[500]="";
	int slen=0;
	FILE *fpIn=NULL,*fpOut=NULL;
	
	if (fpIn=fopen(outFileName, "r"))
	{
		if ((fpOut = fopen(outCflowFname, "w"))==NULL)
		{
			printf("cannot create file %s!\n",outCflowFname);
			return 1;
		}
		printf("generated file: cflow_fc.txt!\n");
		while ((fgets(sReadLine,MAX_LEN,fpIn)!=NULL)&&(!feof(fpIn))) //按行进行处理
		{
			char stemp[100]="",ztemp[10]="";
			int i=0,funs=0,k=0,fune=0;
			
			slen=strlen(sReadLine);
			sReadLine[slen-1]=='\0';
			memset(stemp,0,sizeof(stemp));
			
		//while(sReadLine[i]==' ' && sReadLine[i]!='\0') i++;	//get function name start
			while(sReadLine[i]!=')' && sReadLine[i]!='\0')	//get function name end
			{ 
				stemp[k++]=sReadLine[i];	//get function name
				i++;
			}
			stemp[k++]=sReadLine[i];i++;
			if(sReadLine[slen-2]==':') 
				stemp[k++]=sReadLine[slen-2];
			
			int temj=0;	
			for(temj=slen-3;temj>i;temj--) //get call function start lineNo
				if(sReadLine[temj]==':')
					break;
			if(temj<slen-2)
			{
				int tlen=0;
				for(int t=temj+1;t<slen-2;t++)
				{
					if(sReadLine[t]=='>')
						break;
					ztemp[tlen++]=sReadLine[t];					
				}			
				fprintf(fpOut,"%s %s\n",stemp,ztemp);
			}
			else
				fprintf(fpOut,"%s\n",stemp);
		}
		fclose(fpIn);
		fclose(fpOut);
	}
	else{
		printf("cannot open file %s,pelease make sure file name is correct !\n",outFileName);
		return 1;
	}
	return 0;
}
