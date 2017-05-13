main_get : getHeadFile.o getFunCall.o main_get.o 
	gcc -o main_get main_get.o getHeadFile.o getFunCall.o

getHeaderFile.o : getHeadFile.c 
	gcc -std=c99 -c getHeadFile.c

getFunCall.o : getFunCall.c 
	gcc -std=c99 -c getFunCall.c
	
main_get.o : main_get.c 
	gcc -std=c99 -c main_get.c

clean :
	rm -f *.o *~
