#include <stdio.h>

#define MAX 10

int nunber=0;

void fun_cmp(int a,int b);

int main(int argc, char *argv[])
{
  fun_cmp(1,2);
  return 0;
}

void fun_cmp(int a,int b)
{
  printf("a=%d b=%d\n",a,b);
  if(a>=b)
    printf("Max a:%d\n",a);
  else
    printf("Max b:%d\n",b);
  return;
}
