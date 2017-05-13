KVERS=$(shell uname -r)
MDIR = /lib/modules/$(KVERS)/build

obj-m := globalmem.o

default:
	make -C $(MDIR) M=$(PWD) modules V=1 EXTRA_CFLAGS="-fplugin=gccdiff" 
clean:
	rm *.o *.ko *.mod.c *.order *.symvers
