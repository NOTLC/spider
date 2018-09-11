
from scrapy.cmdline import execute

##调试文件,也就是运行文件的命令包

##os.path.abspath((__file__)当前文件
#当前文件的os.path.dirname上一级目录

#因为需要设置工程的目录所以会用到文件目录的包
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy','crawl','jobbole'])