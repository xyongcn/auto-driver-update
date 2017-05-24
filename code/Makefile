main_get : getHeadFile.o get2ndHdFile.o main_get.o 
	gcc -o main_get main_get.o getHeadFile.o get2ndHdFile.o 

getHeaderFile.o : getHeadFile.c 
	gcc -std=c99 -c getHeadFile.c

get2ndHdFile.o : get2ndHdFile.c 
	gcc -std=c99 -c get2ndHdFile.c
	
main_get.o : main_get.c 
	gcc -std=c99 -c main_get.c

clean :
	rm -f *.o *~
