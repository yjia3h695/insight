from selenium import webdriver
import re
import time

email, passwd = open('login.secret').read().strip().split(',')
cities = ["Boston, MA", "Chicago, IL",
          "Seattle, WA", "DALLAS, TX", "Washington, DC"]
link = "https://www.strava.com/running-races/"
races = []

browser = webdriver.Chrome('chromedriver')
browser.get('https://app.strava.com/login')
browser.find_element_by_name('email').send_keys(email)
browser.find_element_by_name('password').clear()
browser.find_element_by_name('password').send_keys(passwd)
browser.find_element_by_id('login-button').submit()
time.sleep(2)

for r in xrange(len(cities)):
    browser.get(races[r])  # load page
    html_code = browser.page_source.encode('utf-8')
    num_pages = 0
    num = re.search(r'(\d+)<\/a> <a class=\"next_page\"', html_code)
    if num:
        num_pages = int(num.group(1))
    filename = cities[r] + '.html'
    html_file = open(filename, 'w+')
    html_file.write(html_code)
    time.sleep(3)
    for i in xrange(num_pages - 1):
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
    button = browser.find_element_by_xpath(
        '//*[@id="weekly-training-controls"]/div[3]/div')
    for i in xrange(1, 8):
        error2 = False
        while not error2:
            try:
                button.click()
                error2 = True
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//*[@id="weekly-training-controls"]/div[3]/ul/li[' + str(i) + ']').click()
                time.sleep(2)
                html_code = browser.page_source.encode('utf-8')
                html_file.write(html_code)
            except:
                pass
    html_file.close
browser.quit()
