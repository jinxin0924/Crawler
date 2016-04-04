__author__ = 'Xing'

#简单的实现了爬取图片

import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib
url="http://www.meizitu.com/"
path='/Users/Xing/Documents/Crawler/sexy/'
cnt=0 #照片量统计，以及作为图片名称
visited=set()

head = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
response = requests.get(url,headers=head)
soup = BeautifulSoup(response.text,'lxml')
webList=soup.find_all('a',target='_blank')
for webtext in webList:
    # web_url=str(webtext).split(' ')[1].split('=')[1][1:-1]#网页的url
    web_url=webtext['href']
    try:
        if web_url in visited :continue #避免重复
        if 'meizitu' not in web_url:continue #避免连接到外面网
        photo_web=requests.get(web_url,timeout=5)
        visited.add(web_url)
        s=BeautifulSoup(photo_web.text,'lxml')
        photoList=s.find_all('img')
        for photo_text in photoList:
            # photo_url=str(photo_text).split(' ')[2].split('=')[1][1:-3]#照片url
            photo_url=photo_text['src']
            if 'pic.meizitu.com' not in photo_url:continue #避免连接到外面网
            if 'limg' in photo_url:continue #小图
            print(cnt,photo_url,web_url)
            photo = requests.get(photo_url)
            with  open(path+str(cnt),'wb') as newfile:  #图片输出
                newfile.write(photo.content)
            cnt+=1 #照片数量
            print('get'+' '+str(cnt)+'th'+' photo')
        if cnt>50:
            break
    except BaseException as e:
        print(e)
        print('web',webtext)
        print('photo',photo_text)

