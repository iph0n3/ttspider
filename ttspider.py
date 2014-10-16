#--*-code: utf-8 -*-
#author: titans
#date : 2013/11/27


import re
import urllib2
import urllib
import socket
import cookielib
import urlparse
import Queue
import threading
import thread
import time

import sys

lock = threading.RLock()

class MyThread(threading.Thread):
	def __init__(self, unvisited, key, x):
		
		self.unvisited = unvisited
		self.key = key
		
		threading.Thread. __init__(self,name=x)

	def run(self):
		#print 'name:' + self.getName() + '\n'
		
		try:
			sp = Spider()
			#print self.unvisited.qsize()
			
			if self.unvisited.qsize() == 0:	
				thread.exit()
			visitUrl=self.unvisited.get()
			
			global visited
			lock.acquire()
			if visitUrl is None or visitUrl=="" or visitUrl in visited:  #quchong
				lock.release()
				pass
	 		else:
	 			visited.append(visitUrl)
	 			lock.release()

	 			global links
				lock.acquire()
				print visitUrl
				links=links + list(sp.getHyperLinks(visitUrl, self.key))
				lock.release()	
		except:
			
			#print 'Thread error \n'
		 	thread.exit()

		


class Spider():

	def __init__(self):
		#self.visited = []
		self.current_deepth = 1

	def crawling(self, seeds, key, crawl_deepth):
		global urls 
		global jsurls 
		global swfurls
		global picurls
		global cssurls
		global visited 

		global links
		

		urls = []
		jsurls = []
		swfurls = []
		picurls = []
		cssurls = []

		visited = []
		global unvisited
		unvisited = Queue.Queue(10000000)
		if not seeds.startswith('http'):
			seeds = 'http://' + seeds
		unvisited.put(seeds)
		if key == None:
			key = urlparse.urlparse(seeds).netloc
		else:
			key = key



		urls.append(seeds)
	

		while self.current_deepth <= int(crawl_deepth):
			links = []
			t = 0
			while unvisited.qsize()>0:
				thr = []
				for x in range(1024):
					
					thr.append(MyThread(unvisited, key, x))

					thr[x].start()
					if x%12 == 0 and x!= 0: 
						for i in range(t, x):
							
							thr[i].join()
						t = x
					

					if unvisited.qsize() == 0:
						time.sleep(1)
						if unvisited.qsize() == 0:
							break
			
			#print 'link out'

			for link in links:
				if link not in visited:
					unvisited.put(link)
			#print links
			#print 'Path:' + str(self.current_deepth)
 			self.current_deepth += 1

 		#return urls
 		return {'urls':urls,'swfurls':swfurls,'jsurls':jsurls, 'picurls':picurls, 'cssurls':cssurls}
	
	def getHyperLinks(self, url, key):
		
		reurls = []
		
		content = self.geturl(url)

		'''
		@ i think all urls in html only 4 types 
		src=123.html   src=/123.html    src=//host/1.html   src=http://host/1.html
		src='123.html' src='/123.html'  src='//host/1.html' src='http://host/1.html'
		src="123.html" src="/123.html"  src="//host/1.html" src="http://host/1.html" 
		http://host/1.html
		'''


		'''
		@get all urls content http or https
		@result http://www.baidu.com/
		'''
		#pattern = '(https?:\/\/]*[\w\.\/]*)'
		pattern = '(https?:\/\/]*[\w\.\/\-\?\&\%\@\:\,]*)'
		regex = re.compile(pattern)
		gets = regex.findall(content)



		'''
		@get url like src='/cant/get.js'
		@result http://host/cant/get.js 
		'''	
		pattern0 = '(?:href)|(?:src)[\s]*=[\s]*[\'\"]?\/([\w][\w\.\/\-\?\&\%\@\:\,]*)'
		regex0 = re.compile(pattern0)
		gets0 = regex0.findall(content)
		host = re.findall('(https?:\/\/]*[\w\.]*\/?)', url)
		gets0 = [host[0] + i for i in gets0]
		

		'''
		@get url like src='//www.baidu.com/js'
		@result http://www.baidu.com/js
		'''
		pattern1 = '(?:href)|(?:src)[\s]*=[\s]*[\'\"]?(\/\/[\w][\w\.\/\-\?\&\%\@\:\,]*)'
		regex1 = re.compile(pattern1)
		gets1 = regex1.findall(content)
		schem = re.findall('(https?)', url)
		gets1 = [schem[0] + i for i in gets1]



		'''
		@get url like src='1.js'
		@result http://host/js
		'''
		pattern2 = '(?:href)|(?:src)[\s]*=[\s]*[\'\"]?((?!((\/)|(javascript\:)|(https?\:\/\/)|(#)))[\w\.\/\-\?\&\%\@\:\,]*)'
		regex2 = re.compile(pattern2)
		gets2_0 = regex2.findall(content)
		host = re.findall('(https?:\/\/]*[\w\.]*)\/?', url)
		gets2 = []
		for i in gets2_0:
			if '.' in i:
				gets2 = [host[0] + '/' + i for i in gets2_0]
			else:
				continue



		total = gets + gets0 + gets1 + gets2 
		total = set(total)
		total = [i.strip() for i in total]
	

		for i in total:
			url_type = urlparse.urlparse(i).path #add 2014/10/16
			if url_type.endswith('.js'):
				jsurls.append(i)
			elif url_type.endswith('.swf'):
				swfurls.append(i)
			elif url_type.endswith('.jpg') or url_type.endswith('.png') or url_type.endswith('.gif') or url_type.endswith('.ico'):
				picurls.append(i)
			elif url_type.endswith('.css'):
				cssurls.append(i)
			elif key in i:
				urls.append(i)
				reurls.append(i)
			
		#print swfurls
		# print '[+]Total:   %d'%len(total)
		# print '[-]Jsurls:  %d'%len(jsurls)
		# print '[-]Swfurls: %d'%len(swfurls) 
		# print '[-]Urls:    %d'%len(urls)
		
		
		return set(reurls)



	def geturl(self, url):
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.addheaders = [('Cookie', 'Session=11111;a=bbb'), ('Referer', 'http://www.google.com'), ('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0')]
		urllib2.install_opener(opener)
		
		try:
			socket.setdefaulttimeout(5)
			rep = opener.open(url)
			content = rep.read()
		except:
			content = ''
		return content

	