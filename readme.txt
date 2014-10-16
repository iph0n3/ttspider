testnewsp.py 是最新版多线程spider  可以获取普通链接、js文件、swf文件，可以修改返回。


ttspider.py 是我计划入库的，我个人使用的爬虫库用法

import ttspider

spider = ttspier()
dic = spider.run(url,domain,deepth)

返回的是字典做了简单的初步分类
urls 、swfurls、jsurls、picurls、cssurls

将该文件放到C:\Python27\Lib\site-packages 目录下即可以调用