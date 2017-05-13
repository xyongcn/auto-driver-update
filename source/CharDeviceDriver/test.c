#include<stdio.h>
#include<string.h>
#include<fcntl.h>
#define MEM_CLEAR 0x1
#define BUF_LEN 50
int main(void)
{
	int fd,len=0,flen=0;
	char str[BUF_LEN]="hello device drivers on 2016/3/21";
	char buf[BUF_LEN];

	fd=open("/dev/globalmem", O_WRONLY | O_NONBLOCK);

	if(fd!=-1)
	{
		if(write(fd,str,strlen(str))!=-1)
			printf("写入设备成功！\n写入内容：%s\n",str);
		else
			printf("写入失败！\n");
		
		flen=lseek(fd,0,SEEK_CUR);
		printf("文件写入长度：%d\n",flen);

		close(fd);
	}
	else
	{
		printf("设备文件写打开失败！\n");
	}

	fd=open("/dev/globalmem", O_RDONLY | O_NONBLOCK);//
	if(fd!=-1)
	{	
		len=read(fd,buf,flen);	
		buf[len]='\0';
		printf("读取设备内容：%s\n文件读入长度：%d\n",buf,len);
		close(fd);
	}
	else
	{
		printf("设备文件读打开失败！\n");
	}

	fd=open("/dev/globalmem", O_RDONLY | O_NONBLOCK);//
	if(fd!=-1)
	{
		if(ioctl(fd,MEM_CLEAR,0)<0)
			printf("ioctl cmd faild!\n");
		else	printf("ioctl 执行成功, 设备内容已清除！\n");
		close(fd);
	}
	else
	{
		printf("设备文件ioctl操作失败！\n");
	}

	fd=open("/dev/globalmem", O_RDONLY | O_NONBLOCK);//
	if(fd!=-1)
	{	
		len=read(fd,buf,flen);	
		buf[len]='\0';
		len=strlen(buf);
		printf("读取设备内容：%s\n文件读入长度：%d\n",buf,len);
		
		close(fd);
	}
	else
	{
		printf("设备文件读打开失败！\n");
	}
	return 0;
}

