#include<stdio.h>

char foo();
char * foo2(){};

int main()
{
  foo();
  printf("hello world");
  return 0;
}

char foo()
{
	return 'a';
}
