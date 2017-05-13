/**
*增加并发控制的globalmem
*/
#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/errno.h>
#include <linux/mm.h>
#include <linux/sched.h>
#include <linux/cdev.h>
#include <asm/io.h>
#include <asm/uaccess.h>

#define GLOBALMEM_SIZE 0x1000 /*全局内存最大4KB*/
#define MEM_CLEAR 0x1 /*清零全局内存*/
#define GLOBALMEM_MAJOR 230

static int globalmem_major = GLOBALMEM_MAJOR;/*预设de主设备号*/
module_param(globalmem_major, int, S_IRUGO);

/*globalmem的设备结构体：包含了对应于globalmem字符设备的cdev 和 使用内存mem*/
struct globalmem_dev{
 struct cdev cdev;  //cdev结构体
 unsigned char mem[GLOBALMEM_SIZE];  //全局内存
 struct mutex mutex;
};

struct globalmem_dev *globalmem_devp=NULL;  //设备结构体指针

/*文件打开函数*/
static int globalmem_open(struct inode *inode,struct file *filp)
{
 filp->private_data = globalmem_devp; //将设备结构体指针赋值给文件私有数据指针
 printk(KERN_INFO " function globalmem_open running success!\n");
 return 0;
}

/*文件释放函数*/
static int globalmem_release(struct inode *inode,struct file *filp)
{
 printk(KERN_INFO " function globalmem_release running success!\n");
 return 0;
}

/*设备控制函数：ioctl()函数接受的MEM_CLEAR命令，这个命令将全局内存的有效数据长度清零，对于设备不支持的命令，ioctl()函数应该返回-EINVAL*/
static long globalmem_ioctl(struct file *filp,unsigned int cmd,unsigned long arg)
{
 struct globalmem_dev *dev = filp->private_data; 
//获得设备结构体指针
 switch(cmd){
  case  MEM_CLEAR:
	mutex_lock(&dev->mutex);//
    memset(dev->mem,0,GLOBALMEM_SIZE);
    printk(KERN_INFO "globalmem is set to zero.\n");
	mutex_unlock(&dev->mutex);//
   break;
  default:
   return -EINVAL;
 }
 printk(KERN_INFO " function globalmem_ioctl running success!\n");
 return 0;
}

/*读函数：读写函数主要是让设备结构体的mem[]数组与用户空间交互数据，并随着访问字节数变更返回用户的文件读写偏移位置*/
static ssize_t globalmem_read(struct file *filp,char __user *buf,size_t size,loff_t *ppos)
{
 unsigned long p = *ppos;
 unsigned int count = size;
 int ret = 0;
 struct globalmem_dev *dev = filp->private_data; 
 
 if(p >= GLOBALMEM_SIZE)  //分析和获取有效的长度
 {
  return 0;
 }
 if(count > GLOBALMEM_SIZE - p)
 {
  count = GLOBALMEM_SIZE - p;
 }
 
 mutex_lock(&dev->mutex);// mutex locked

 if(copy_to_user(buf,dev->mem+p,count))  //内核空间->用户空间
   ret = -EFAULT;
 else{
  *ppos += count;
  ret = count;
  printk(KERN_INFO "read %u bytes(s) from %lu.\n",count,p);
 }
 printk(KERN_INFO " function globalmem_read running success!\n");
 
 mutex_unlock(&dev->mutex);//mutex unlocked 

 return ret;
}

/*写函数*/
static ssize_t globalmem_write(struct file *filp,const char __user *buf,size_t size,loff_t *ppos)
{
 unsigned long p = *ppos;
 unsigned int count = size;
 int ret=0;
 
 struct globalmem_dev *dev = filp->private_data;
 
 if(p >= GLOBALMEM_SIZE)  //分析和获取有效的写长度
 {
  return 0;
 }
 
 if(count > GLOBALMEM_SIZE - p)
 {
  count = GLOBALMEM_SIZE - p;
 }
 
 mutex_lock(&dev->mutex);//

 if(copy_from_user(dev->mem + p,buf,count)) // 用户空间->内核空间
  ret = -EFAULT;
 else{
  *ppos =+ count;
  ret = count;
  printk(KERN_INFO"written %u bytes(s) from %lu.\n",count,p);
 }
 printk(KERN_INFO " function globalmem_write running success!\n");

 mutex_unlock(&dev->mutex);//

 return ret;
}

/*seek文件定位函数：seek()函数对文件定位的起始地址可以是文件开头(SEEK_SET,0)、当前位置(SEEK_CUR,1)、文件尾(SEEK_END,2)*/
static loff_t globalmem_llseek(struct file *filp,loff_t offset,int orig)
{
 loff_t ret = 0;

 switch(orig)
 {
  case 0:   //相对文件开始位置偏移
   if(offset <0 )
   {
    ret = -EINVAL;
    break;
   }
   
   if((unsigned int )offset > GLOBALMEM_SIZE)
   {
    ret = - EINVAL;
    break;
   }
   filp->f_pos = offset;
   ret = filp->f_pos;
   break;
   
  case 1:   //相对文件当前位置偏移
   if((filp->f_pos + offset) > GLOBALMEM_SIZE)
   {
    ret = -EINVAL;
    break;
   }
   if((filp->f_pos + offset)<0)
   {
    ret = -EINVAL;
    break;
   }
   filp->f_pos +=offset;
   ret = filp->f_pos;
   break;

  case 2:   //相对文件END位置偏移
   if(offset >0 )
   {
    ret = -EINVAL;
    break;
   }
   
//   if((unsigned int )offset*(-1) > GLOBALMEM_SIZE)
   if ((filp->f_pos + offset)<0)
   {
    ret = - EINVAL;
    break;
   }

   filp->f_pos += offset;
   ret = filp->f_pos;
   break;

  default:
   ret = -EINVAL;
   break; 
 }
 printk(KERN_INFO " function globalmem_llseek running success!\n");
 return ret;
}

/*文件操作结构体*/
static const struct file_operations globalmem_fops={
 .owner = THIS_MODULE,
 .llseek = globalmem_llseek,
 .read = globalmem_read,
 .write = globalmem_write,
 .unlocked_ioctl = globalmem_ioctl,
 .open = globalmem_open,
 .release = globalmem_release,
};

/*初始化并注册cdev*/
static void globalmem_setup_cdev(struct globalmem_dev *dev,int index)
{
 int err,devno = MKDEV(globalmem_major,index);

 cdev_init(&dev->cdev,&globalmem_fops);
 dev->cdev.owner = THIS_MODULE;
 //dev->cdev.ops = &golbalmem_fops;
 err = cdev_add(&dev->cdev,devno,1);
 if(err)
  printk(KERN_NOTICE"Error:%d adding globalmem%d",err,index);

 printk(KERN_INFO " function globalmem_setup_cdev running success!\n");
}

/*设备驱动模块加载函数*/
static int __init globalmem_init(void)
{
 int ret;
 dev_t devno = MKDEV(globalmem_major,0);
 
 if(globalmem_major) //申请设备号
  ret = register_chrdev_region(devno,1,"globalmem");
 else{  //动态申请设备号
  ret = alloc_chrdev_region(&devno,0,1,"globalmem");
  globalmem_major = MAJOR(devno);
 }

 if(ret < 0)
  return ret;
 //申请设备结构体的内存
 globalmem_devp = kzalloc(sizeof(struct globalmem_dev),GFP_KERNEL); 

 if(!globalmem_devp){
  ret = -ENOMEM;
  goto fail_malloc;
 }
 
 //memset(globalmem_devp,0,sizeof(struct globalmem_dev));
 mutex_init(&globalmem_devp->mutex);//增加并发控制
 globalmem_setup_cdev(globalmem_devp,0);

 printk(KERN_INFO " function globalmem_init running success!\n");

 return 0;
 
 fail_malloc:
	unregister_chrdev_region(devno,1);
 	return ret;
}
module_init(globalmem_init);

/*模块卸载函数*/
static void __exit globalmem_exit(void)
{
 cdev_del(&globalmem_devp->cdev); //注销cdev
 kfree(globalmem_devp);          //释放设备结构体内存
 unregister_chrdev_region(MKDEV(globalmem_major,0),1); //释放设备号
 
 printk(KERN_INFO " function globalmem_exit running success!\n");

}
module_exit(globalmem_exit); 

MODULE_AUTHOR("Ryy");
MODULE_LICENSE("GPL v2");

