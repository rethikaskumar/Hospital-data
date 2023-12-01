# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 09:36:18 2022

@author: maana lisa
"""

import requests
from bs4 import BeautifulSoup
#from gensim.summarization import summarize
import json
import re

def getdata():
    
    #KMCH
    
    url='https://kmchhospitals.com/kmch-main-center/'

    page=requests.get(url).text
    #turing page to beautiful soup object

    soup=BeautifulSoup(page,features="html.parser")

    #using google inspect tool we find headline is of <h1> tag
    headline=soup.find('h2').get_text()
    docField=soup.find('h4').get_text() 
    docName=soup.find('a').get_text()
    listOfSpl=soup.find('ul').get_text()

    #main article contains <p> tags 
    h4Tag=soup.find_all('h4')
    aTag=soup.find_all('a')
    ulTag=str(soup.find_all('ul'))
    
    result=ulTag.split('</ul>')
    result=[i for i in result if 'Dr' in i]
    for j in range(6):
        result=[i for i in result if result.index(i)!=5]
    for j in range(2):
        result=[i for i in result if result.index(i)!=12]
    for j in range(2):
        result=[i for i in result if result.index(i)!=17]
    
    docFields=[tag.get_text().strip() for tag in h4Tag]
    docNames=[tag.get_text().strip() for tag in aTag]
    
    #removing author name
    specializations=[string for string in docFields if not '\n' in string]

    finallist=[]
    doclist=[]
    specializations=[i for i in specializations if specializations.index(i)!=4]
    specializations=[i for i in specializations if specializations.index(i)!=5]
    specializations=[i for i in specializations if specializations.index(i)!=12]
    specializations=[i for i in specializations if specializations.index(i)!=17]

    for i in range(len(result)):
      
        list1=result[i].split('</li>')
        if (i==9 or i==10):
            list1=list1[:-2]
        else:
            list1=list1[:-1]

        if i==31:
            list1=[doc for doc in list1 if list1.index(doc)!=1]
        namelist=[]
        for j in range(len(list1)):
          #URLless_string = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', j)
            list2=list1[j].split("Dr")
            list2[1]=list2[1].strip(',</a>')
          
            namelist.append("Dr"+list2[1])
        doclist.append(namelist)
    
    
    kmchDict=dict((k, v) for k in specializations for v in doclist if specializations.index(k)==doclist.index(v))
    
    #-----------------------------------------------------
    #SHEELA
    #Sheela hosptital

    doclist=[]
    def createBS(url,splname):
        page=requests.get(url).text
        soup=BeautifulSoup(page,features="html.parser")

        info=soup.find('td').get_text()
        tdTag=soup.find_all('td')
        spl=[tag.get_text().strip() for tag in tdTag]
        docs=[string for string in spl if not '\n' in string]
        docs=[string for string in spl if '.' in string]
        docName=[]
        for i in docs:
            i1=i.split("                              ")
            lenList=len(i1)
            docName.append(i1[0])  
        doclist.append(docName)

    baseUrl="http://www.sheelahospital.in/department/"
    spl=["gynaecology","department-of-medicine","emergency-medical-trauma","medicine"]
    for i in range(4):
        url=baseUrl+spl[i]+"/"
        createBS(url,spl[i])
    sheelaDict=dict((k,v) for k in spl for v in doclist if spl.index(k)==doclist.index(v))

    #-----------------------------------------------------
    #Ramakrishna
    url="https://www.sriramakrishnahospital.com/doctors/"
    page=requests.get(url).text
    #turing page to beautiful soup object
    soup=BeautifulSoup(page,features="html.parser")
    docField=soup.find('h3').get_text()
    docName=soup.find('h2').get_text()
    docInfo=soup.find('a').get_text()

    h3Tag=soup.find_all('h3')
    h2Tag=soup.find_all('h2')
    aTag=soup.find_all('a')

    spl=[tag.get_text().strip() for tag in h3Tag]
    docNames=[tag.get_text().strip() for tag in h2Tag]
    docinfo=[tag.get_text().strip() for tag in aTag]
    specializations=spl[3:44]
    
    names=[string for string in docNames if not '\n' in string]
    names=[string for string in docNames if '.' in string]
    names=[string for string in names if 'Dr' in string]

    docInfo=[string for string in docinfo if not '\n' in string]
    docInfo=[string for string in docinfo if '.' in string]
    finalInfo1=[]
    finalInfo=[]
    for i in docInfo:
      table=i.maketrans("\t"," ")
      finalInfo1.append(i.translate(table))
    for i in finalInfo1:
      table=i.maketrans("\n"," ")
      finalInfo.append(i.translate(table))
   
    RamaDict={}
    for i in specializations:
      doc=[]
      for n in finalInfo:
        if i[0:10] in n:
          doc.append(n)
      RamaDict.update({i:doc})

    Hlist=[kmchDict, sheelaDict, RamaDict]
    
    with open ("docdata.json", "w") as file:
        json.dump(Hlist, file)


getdata()  