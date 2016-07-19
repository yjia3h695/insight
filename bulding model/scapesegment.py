# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 23:03:49 2016

@author: yanxin
"""
from selenium import webdriver
import re
import time
from bs4 import BeautifulSoup
import os
import errno


email, passwd,db_name,db_user,db_pswd = open('login.secret').read().strip().split(',')

cities = ["Boston, MA","Chicago, IL","Seattle, WA","DALLAS, TX","Washington, DC"]

browser = webdriver.Chrome('/home/yanxin/Desktop/chromedriver')
browser.get('https://app.strava.com/login')
browser.find_element_by_name('email').send_keys(email)
browser.find_element_by_name('password').clear()
browser.find_element_by_name('password').send_keys(passwd)
browser.find_element_by_id('login-button').submit()
time.sleep(2)

browser.get('https://www.strava.com/segments/search')

for i in xrange(len(cities)):
    browser.get('https://www.strava.com/segments/search')
    browser.find_element_by_name('keywords').clear()
    browser.find_element_by_name('keywords').send_keys(cities[i])
    browser.find_element_by_id('climb-search-button').submit() 
    time.sleep(2)
    
    html_code = browser.page_source.encode('utf-8')
    
    soup = BeautifulSoup(html_code, 'html.parser')
    segmentList = []
    urlList = []
    for link in soup.find_all('div'):
        segment = link.get('data-segment-id')         
        if segment:
           segmentList.append(segment)
           urlList.append('https://www.strava.com/segments/'+segment)
           
    for r in xrange(len(segmentList)-1):
        num_pages = 0
        browser.get(urlList[r])
        html_code = browser.page_source.encode('utf-8')
        num = re.search(r'(\d+)<\/a> <a class=\"next_page\"',html_code)
        if num: num_pages = int(num.group(1))
        filename='/data/'+cities[i]+'+'+segmentList[r]+'.html'
        if not os.path.exists(os.path.dirname(filename)):
           try:
               os.makedirs(os.path.dirname(filename))
           except OSError as exc: # Guard against race condition
               if exc.errno != errno.EEXIST:
                  raise
        html_file = open(filename,'w+')
        html_file.write(html_code)
       
        for n in xrange(num_pages-1):
            time.sleep(1)
            error = False
            while not error:
                try:
                    browser.find_element_by_class_name("next_page").click()
                    error = True
                except:
                    pass
                time.sleep(1)
            html_code = browser.page_source.encode('utf-8')
            html_file.write(html_code)     
            html_file.close
browser.quit() 