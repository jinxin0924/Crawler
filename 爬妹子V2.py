__author__ = 'Xing'

# 在v2中，要实现：1）爬取全部图片



import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib
from collections import deque

url = "http://www.meizitu.com/"
path = '/Users/Xing/Documents/Crawler/sexy/'


visited = set()  #存放已经爬取过的网址
stack = deque()  #存放要探索的网址
stack.append(url)  #初始
nameSet=set() #存放已经爬取过的图片名称
TimeOut=5
head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
totalCnt=0
while stack:
    try:
        url=stack.popleft()
        visited.add(url)
        response = requests.session().get(url,headers=head,timeout=TimeOut)
        soup = BeautifulSoup(response.content, 'lxml')
        webList = soup.find_all('a')
        for webText in webList:
            web_url = webText.get('href')
            if web_url and web_url not in visited: #web_url 非空加入stack
                stack.append(web_url)
        #查看该页面是否有图片
        photoList=soup.find_all('img')
        for photoText in photoList:
            photoUrl = photoText.get('src')
            if 'erweima' in photoUrl:continue #不要二维码的图片
            if 'limg' in photoUrl:continue#不要小图
            if 'templets' in photoUrl:continue #不要模板图
            photoName=photoText.get('alt')
            photoStoreName=photoUrl.split('uploads')[1]
            if photoName and photoUrl and photoStoreName not in nameSet:
                photo = requests.session().get(photoUrl,headers=head,timeout=TimeOut)
                with open(path+photoName,'wb') as newfile:  #图片输出
                    newfile.write(photo.content)
                nameSet.add(photoStoreName) #存入名称
                if totalCnt%20==0:print('get'+' '+str(totalCnt)+'th'+' photo')
                totalCnt+=1
        if totalCnt>100:
            break
    except BaseException as e:
        print(e)
