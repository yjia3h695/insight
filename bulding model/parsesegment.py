# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 23:03:49 2016

@author: yanxin
"""
from sqlalchemy import create_engine
from selenium import webdriver
import time
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import re

email, passwd,db_name,db_user,db_pswd = open('login.secret').read().strip().split(',')

cities = ["Boston, MA","Chicago, IL","Seattle, WA","DALLAS, TX"]

browser = webdriver.Chrome('/home/yanxin/Desktop/chromedriver')
browser.get('https://app.strava.com/login')
browser.find_element_by_name('email').send_keys(email)
browser.find_element_by_name('password').clear()
browser.find_element_by_name('password').send_keys(passwd)
browser.find_element_by_id('login-button').submit()

A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
G=[]
H=[]
I=[]
J=[]
stat1=[]
stat2=[]
stat3=[]
stat4=[]
stat5=[]
Loca=[]
ath_page=[]
latitude = []
longitude = []

for i in xrange(len(cities)):
    browser.get('https://www.strava.com/segments/search')
    browser.find_element_by_name('keywords').clear()
    browser.find_element_by_name('keywords').send_keys(cities[i])
    browser.find_element_by_id('climb-search-button').submit() 
    time.sleep(2)
    
    html_code = browser.page_source.encode('utf-8')
    Soup = BeautifulSoup(html_code, 'html.parser')       
    segmentList = []
    urlList = []    
            
    for link in Soup.find_all('div'):
        segment = link.get('data-segment-id')         
        if segment:
           segmentList.append(segment)
           urlList.append('https://www.strava.com/segments/'+segment)
           
    for r in xrange(len(segmentList)-1):
        
        filename='data/'+cities[i]+'+'+segmentList[r]+'.html'
        f = open(filename,'rU')
        soup = BeautifulSoup(f, 'html.parser')      
               
        statsGroup=soup.find('ul',class_="inline-stats list-stats")
        
        states = statsGroup.find_all('b',class_="stat-text")
        stata  = states[0].text.strip('mi')
        statb  = states[1].text.strip('%')
        statc  = states[2].text.strip('ft')
        statd  = states[3].text.strip('ft')
        state  = states[4].text.strip('ft')
        
        jsgroups= soup.find_all('script')
        regex =  re.compile(r'"lat_lng":\[(\d+.\d+),(\-\d+.\d+)]')
        
        lat= None
        lng= None
        for js in jsgroups:
            text = js.text
            js_text = re.search(regex, text)
            if js_text:
                found=js_text        
                lat = float(found.group(1))
                lng = float(found.group(2))
        
        locations=soup.find_all('span')
        for li in locations:
            if li.get('data-full-name') is not None:
                location = li.get('data-full-name')  

        right_table=soup.find_all('table', class_='striped')
        
        for table in right_table:
            for row in table.findAll('tr'):
                cells = row.findAll('td')
                states = row.findAll('th') 
                if len(cells)==8: #Only extract table body not heading
                    A.append(cells[0].text.strip('\n'))                    
                    B.append(cells[1].find('a').text)
                    ath_link=cells[1].find('a',href=True)['href']
                    ath_page.append('https://www.strava.com'+ath_link)
                    day = cells[2].find('a').text
                    date=datetime.datetime.strptime(day,'%b %d, %Y').date
                    C.append(date)
                    D.append(cells[3].text.strip('mi/h'))
                    E.append(cells[4].text.strip('\n').strip('bpm').strip('-'))
                    F.append(cells[5].text.strip('\n').strip('W'))
                    G.append(cells[6].text.strip('\n').strip('-'))
                    H.append(cells[7].text.strip('s'))
                    I.append(cities[i])
                    J.append(segmentList[r])
                    stat1.append(stata)
                    stat2.append(statb)
                    stat3.append(statc)
                    stat4.append(statd)
                    stat5.append(state)
                    Loca.append(location)
                    latitude.append(lat)
                    longitude.append(lng)                   
                                              
browser.quit() 

df=pd.DataFrame(A,columns=['rank'])
df['name']=B
df['date']=C
df['pace']=D
df['hr']=E
df['power']=F
df['vam']=G
df['time']=H
df['city']=I
df['segment']=J
df['distance']=stat1
df['avg_grade']=stat2
df['lowest_elev']=stat3
df['highest_elev']=stat4
df['elev_difference']=stat5
df['segment_name']=Loca
df['athlete_link']=ath_page
df['latitude']=latitude
df['longitude']=longitude
df['date'] = pd.to_datetime(df['date'].astype(str))

engine = create_engine('postgresql://%s:%s@localhost/%s'%(db_user,db_pswd,db_name))

## insert data into database from Python
df.to_sql('running_data_table', engine, if_exists='replace')