__author__ = 'Xing'

# 在v3中，要实现：1）采用多进程爬取图片
#会有timeout错误，还有 Max retries exceeded with url: /a/nvshen.html (Caused by ConnectTimeoutError(<requests.packages.urllib3.connection.HTTPConnection object at 0x1065007f0>, 'Connection to www.meizitu.com timed out. (connect timeout=5)'))
#应该都是网络问题


import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib
from collections import deque
from multiprocessing import Pool,Manager,Queue,Lock


def process(url,totalCnt,visited,nameSet):
    stack = deque()   #存放要探索的网址
    stack.append(url)
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
                    if totalCnt['cnt']%100==0:print('get'+' '+str(totalCnt['cnt'])+'th'+' photo')
                    totalCnt['cnt']+=1

        except BaseException as e:
            print(e)


if __name__ == '__main__':
    url = "http://www.meizitu.com/"
    path = '/Users/Xing/Documents/Crawler/sexy/'
    visited = set()  #存放已经爬取过的网址
    # stack = Queue()  #存放要探索的网址
    # stack.put(url)  #初始
    nameSet=set() #存放已经爬取过的图片名称
    TimeOut=5
    head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    totalCnt=Manager().dict()
    totalCnt['cnt']=0
    p=Pool(4)
    # lock=Lock()
    response = requests.session().get(url,headers=head,timeout=TimeOut)
    soup = BeautifulSoup(response.content, 'lxml')
    webList = soup.find_all('a')
    for webText in webList:
        web_url = webText.get('href')
        if web_url and web_url not in visited: #web_url 非空加入stack
            p.apply_async(process,args=(url,totalCnt,visited,nameSet))
    p.close()
    p.join()
