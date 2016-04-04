import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib

url="https://movie.douban.com/top250?"
titleList=[]
ratingList=[]

for page in range(10):
    dict_word={'start':page*25}
    full_url=url+urllib.parse.urlencode(dict_word) #得到url
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text,'lxml')
    result=soup.find_all(attrs={"class": "title"}) #得到title的list
    for i in result:
        title=i.string
        if '/' in title :continue
        titleList.append(title)
        
    rating_result=soup.find_all(attrs={"class": "rating_num"}) #得到rating的list
    for i in rating_result:
        rating=i.string
        ratingList.append(rating)
        
for i in range(len(ratingList)):
    print('Top'+str(i+1),titleList[i],ratingList[i])