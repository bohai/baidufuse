baidufuse
=========

fuse base on baidu cloud storage

基于fuse实现的一个文件系统，后端使用baidu网盘。（其他的网盘应该也可以，先拿这个玩玩吧）

依赖的库：  
1.baidupan (baidu网盘API的python binding)  
https://github.com/solos/baidupan  

2.fuse python(fuse的python binding)  
http://sourceforge.net/apps/mediawiki/fuse/?title=FUSE_Python_tutorial

3.fuse

==========

使用：  
1. 填写baidufuseconf.py中的token和rootdir。（从baidu pcs上获取token和设置rootdir)  
2. 使用命令baidufuse挂载到某个目录  
baidufuse  mnt/  
3. 所挂载的目录可以看到百度盘上的文件，目录。  

备注：  
目前未实现写文件的功能。  
