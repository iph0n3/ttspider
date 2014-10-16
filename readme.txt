
ttspider.py 是我计划入库的，我个人使用的爬虫库

用法

import ttspider

spider = ttspier()
dic = spider.run(url,domain,deepth)

返回的是字典做了简单的初步分类
urls 、swfurls、jsurls、picurls、cssurls
{'urls':urls, 'swfurls':swfurls, 'jsurls':jsurls, 'cssurls':cssurls}

将该文件放到C:\Python27\Lib\site-packages 目录下即可以调用