################################################################################
# Crawl Av Company profiles from collection CompanyAV
################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from pyvirtualdisplay import Display
from random import randint
from datetime import datetime
import sys, time, random
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def login(browser):
    try:
        browser.quit()
    except:
        pass
    #binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
    #browser = webdriver.Firefox(firefox_binary=binary)
    browser = webdriver.Firefox()
    #time.sleep(5)
    browser.get('http://app.avention.com')
    user = browser.find_element_by_id('username')
    user.send_keys('user')
    password = browser.find_element_by_id('password')
    password.send_keys('avention1')
    password.send_keys(u'\ue007')
    time.sleep(5)
    print "Logged in"
    print browser.current_url
    return browser

Display = Display(visible = 0, size = (800, 600))
Display.start()

browser = ''
browser = login(browser)
#browser.implicitly_wait(10)
client = MongoClient('mongodb://ip:port')
CompanyAV = client.Avention.CompanyAV
filter = {'$and' : [{'status' : {'$exists' : False}}, {'priority' : 0}]}
cursor = CompanyAV.find(filter, no_cursor_timeout = True)
for doc in cursor:
    browser.get(doc['aventionUrl'])
    time.sleep(random.random())
    data = {}
    try:
        elt = WebDriverWait(browser, 5).until\
        (EC.presence_of_element_located((By.XPATH, './/div[@class="left-info pull-left"]')))
    except:
        continue
    try:
        tmp = elt.find_element_by_xpath\
        ('.//div[@class="company-address primary"]').text
        tmp = tmp.split('\n')
        data['location'] = tmp[1].rsplit(',', 1)[0]
        data['country'] = tmp[2]
    except:
        pass
    try:
        data['website'] = elt.find_element_by_xpath('.//span[@class="data-value long-line url"]').text
    except:
        pass
    try:
        social = elt.find_element_by_xpath('.//div[@class="social-container"]')
        data['facebookUrl'] =  social.find_element_by_xpath\
        ('.//div[@class="search-result-facebook search-result-social"]/a').get_attribute('href')
        if 'search' in data['facebookUrl']:
            data['facebookUrl'] = None
        data['twitterUrl'] = social.find_element_by_xpath\
        ('.//div[@class="search-result-twitter search-result-social"]/a').get_attribute('href')
        if 'search' in data['twitterUrl']:
            data['twitterUrl'] = None
        data['linkedinUrlId'] =  social.find_element_by_xpath\
        ('.//div[@class="search-result-linkedin search-result-social"]/a').get_attribute('href')
        if 'vsearch' in data['linkedinUrlId']:
            data['linkedinUrlId'] = None
        #print Facebook, Twitter, Linkedin
    except:
        pass
    #orgType,  Industry, sales,  Location, 
    try:
        data['employeeCount'] = elt.find_element_by_xpath\
        ('.//div[@class="data-container"]/span[contains(text(), "Employees")]/following-sibling::span').text
        #print Employees
    except:
        pass
    try:
        data['orgType'] = elt.find_element_by_xpath \
        ('.//div[@class="data-container"]/span[contains(text(), "Company orgType")]/following-sibling::span').text
        #print orgType
    except:
        pass
    try:
        data['parent'] = elt.find_element_by_xpath \
        ('.//div[@class="data-container"]/span[contains(text(), "Parent")]/following-sibling::span/a').get_attribute('href')
        #print orgType
    except:
        pass
    try:
        data['corporateFamily'] = elt.find_element_by_xpath \
        ('.//div[@class="data-container"]/span[contains(text(), "Corporate Family")]/following-sibling::span/a').get_attribute('href')
        #print orgType
    except:
        pass
    try:
        data['industry'] = elt.find_element_by_xpath \
        ('.//div[@class="data-container"]/span[contains(text(), "Industry")]/following-sibling::span').text
        #print Industry
    except:
        pass
    try:
        data['sales'] = elt.find_element_by_xpath \
        ('.//div[@class="data-container"]/span[contains(text(), "Annual Sales")]/following-sibling::span').text
        #print Sales
    except:
        pass
    try:
        data['aventionId'] = elt.find_element_by_xpath \
        ('.//div[@class="data-container"]/span[@class="data-label wide"]/following-sibling::span').text
        #print Avention_ID
    except:
        pass
    try:
        data['totalContacts'] = browser.find_element_by_xpath('.//span[@id="totalContacts"]').text
    except:
        pass
    try:
        elt = WebDriverWait(browser, 2).until(EC.presence_of_element_located \
              ((By.XPATH, './/td[@class="category-content"]')))
        data['description'] = elt.text
    except:
        pass
    fout = open('Avention/Company/' + str(doc['_id']) + '.html', 'w')
    fout.write(browser.page_source.encode('utf-8'))
    fout.close()
    #companyContacts = browser.current_url.rsplit('_', 1)[0] + '_contacts'
    #browser.get(companyContacts)
    try:
        companyContacts = WebDriverWait(browser, 5).until(EC.presence_of_element_located\
                                            ((By.XPATH, './/a[@id="company_contacts"]')))
        companyContacts.click()
    except:
        pass
    time.sleep(5)
    aventionContacts = []
    for person in browser.find_elements_by_xpath('.//div[@class="search-result-container contact-result row-fluid"]'):
        tmp = {}    
        tmp['name'] = person.find_element_by_xpath('.//div[@class="name-row"]').text
        tmp['designation'] = person.find_element_by_xpath\
        ('.//span[@class="large-black-text contact-title"]').text[:-3]
        tmp['location'] =  person.find_element_by_xpath\
        ('.//div[@class="location"]').text.split('\n')[0]
        social = person.find_element_by_xpath('.//div[@class="social-row"]')
        tmp['facebookUrl'] = social.find_element_by_xpath\
        ('.//div[@class="search-result-facebook search-result-social  pull-right"]/a').get_attribute('href')
        if 'search' in tmp['facebookUrl']:
            tmp['facebookUrl'] = None
        tmp['twitterUrl'] =  social.find_element_by_xpath\
        ('.//div[@class="search-result-twitter search-result-social  pull-right"]/a').get_attribute('href')
        if 'search' in tmp['twitterUrl']:
            tmp['twitterUrl'] = None
        tmp['linkedinUrlId'] =  social.find_element_by_xpath\
        ('.//div[@class="search-result-linkedin search-result-social  pull-right"]/a').get_attribute('href')
        if 'vsearch' in tmp['linkedinUrlId']:
            tmp['linkedinUrlId'] = None
        try:
            tmp['email'] = person.find_element_by_xpath('.//a[@class="black-text"]').text
        except:
            pass
        aventionContacts.append(tmp)
    if aventionContacts != []:
        fout = open('Avention/Contact/' + str(doc['_id']) + '.html', 'w')
        fout.write(browser.page_source.encode('utf-8'))
        fout.close()
    data['aventionContacts'] = aventionContacts
    if data:
        print doc['name']
        #print data
        data['lastModified'] = datetime.utcnow()
        data['status'] = 2
        CompanyAV.update({'_id' : doc['_id']}, {'$set' : data})
cursor.close()
browser.quit()
Display.stop()

