KMPATH =/lib/modules/$(shell uname -r)/build  #module build path
INCLUDE =-I/home/ryyan/SOURCE/linux-3.5.4/include

pcnet-objs := pcnet32.o
#obj-$(CONFIG_PCNET32) += pcnet32.o
obj-m += pcnet32.o

all:
	make -C  $(KMPATH) M=$(PWD) modules $(INCLUDE) V=1 EXTRA_CFLAGS="-fplugin=gccdiff"
clean:
	make -C $(KMPATH) M=$(PWD) clean
	rm -f *~
	rm *.mod.c.ind


