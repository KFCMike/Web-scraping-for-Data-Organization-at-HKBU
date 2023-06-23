import pandas as pd
import math
from bs4 import BeautifulSoup
import requests

url= "https://www.math.hkbu.edu.hk/colloquium-all.php"
page = requests.get(url)
#print(page.text)
soup =  BeautifulSoup(page.content,"html.parser")
lev1=soup.find('div', class_='about-content')
#lins=linss.find_all('a')

lev2 = []
for levs in lev1.find_all('a'):
    lev2.append(levs.get('href'))

lev2.pop()

final = {
  "date":[],
  "title": [],
  "speaker": [],
  "speakerorg": [],
  "time/place": [],
  "abstract" : []
}

t="title"
s="speaker"
tp="time/place"
a="abstract"
m="date"
so="speakerorg"

da=""
mo=""
ye=""
ss=[]
da1=""
da2=""

for ind in range(len(lev2)):
    page2 = requests.get("https://www.math.hkbu.edu.hk"+lev2[ind])
    soup2 =  BeautifulSoup(page2.content,"html.parser")
    lev3=soup2.find('div', class_='about-content')
    lev4=lev3.find('ul')
    lev5=lev4.find('li')
    lev5c=lev4.find_all('li')
    lev6b=lev5.find_all('b')
    
    ss=lev2[ind]
    ye=ss[25:29]
    if ss[37]=='&':
        mo="0"+ss[36]
    else:
        mo=ss[36:38]

    for iiter2 in range(len(lev5c)):
        lev6=lev5c[iiter2]
        lev6td=lev6.find_all('td')
        if len(lev5c) != (iiter2+1):
            lev61=lev5c[iiter2+1]
            lev61td=lev61.find_all('td')
        
        ss=lev6b[iiter2].get_text()
        
        for ii in range(len(ss)):
            if ss[ii].isdigit():
                da2=ss[ii]
                da1="0"
                if ss[ii+1].isdigit():
                    da1=ss[ii]
                    da2=ss[ii+1]
                break
                
        #print date of the colloquium
        #da=da1+da2+"/"+mo+"/"+ye
        #print(da1+da2+"/"+mo+"/"+ye)
        
        ss=[]
        da1=""
        da2=""
        
        final[m].append(da)
        final[t].append(lev6td[1].get_text())
        
        ss=lev6td[3].get_text()
        lss=len(ss)
        

        commas=0
        for ii in range(lss):
            if ss[ii]==",":
                final[s].append(ss[:ii])
                final[so].append(ss[(ii+1):])
                commas=commas+1
                break
        if commas==0:
            final[s].append(ss)
            final[so].append("")
        
        commas=0
        ss=[]
        da1=""
        da2=""
        final[tp].append(lev6td[5].get_text())
        
        if len(lev5c) != (iiter2+1):
            if (len(lev6td)-len(lev61td))==10:
                final[a].append(lev6td[9].get_text())
            else:
                final[a].append("empty")
        else:
            if len(lev6td)==10:
                final[a].append(lev6td[9].get_text())
            else:
                final[a].append("empty")

data1 = pd.DataFrame(final)
excel2 = pd.ExcelWriter("HKBUMATHcolloquium.xlsx",engine='xlsxwriter')
data1.to_excel(excel2,sheet_name="sheet1")
excel2.save()
