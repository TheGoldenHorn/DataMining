################################################################################
#  Crawl Linkedin Company Pages and Store in 'CompanyED'
################################################################################

import os, json, time, socket, random, sys
from random import randint
from pymongo import MongoClient
from datetime import datetime
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
#Import the Proxy class from the selenium library
#from selenium.webdriver.common.proxy import *
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#global Users
Display = Display(visible=0, size=(800, 600))
#browser = webdriver.firefox()

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# login to linkedin.com
def login(browser):
    try:
        browser.close()
    except:
        pass
    #binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
    #browser = webdriver.Firefox(firefox_binary=binary)
    browser = webdriver.Firefox()
    browser.get('https://www.linkedin.com/')
    user = browser.find_element_by_id('login-email')
    password = browser.find_element_by_id('login-password')
    username = 'user' 
    print username
    user.send_keys('user')
    password.send_keys('pass')
    password.send_keys(Keys.RETURN)
    time.sleep(5)

    if 'account-restricted' in browser.current_url:
        print 'User is blocked (time to create new linkedin user)!!'
        sys.exit()
    elif 'consumer-email-challenge' in browser.current_url:
        print 'User need signin verification !!'
        sys.exit()
    elif 'captcha' in browser.current_url:
        print 'User need captcha verification !!'
        sys.exit()
    else:
        pass
    return browser

# scrap data from company profiles
def get_data(link, browser):
    url = link
    try:
        browser.get(url)
        #if not link == browser.current_url:
            #return link
    except:
        browser = login(browser)
        browser.get(url)
    time.sleep(2)
    c_url = browser.current_url
    print c_url	
    if 'company-beta' in c_url:
        #org-top-card-module__details
        print c_url
        try:
            browser.find_element_by_xpath('//button[@class="org-about-company-module__show-details-btn"]').click()
        except:
            pass
        tmp = {}
        try:
            tmp['name'] = browser.find_element_by_xpath('//h1[@class="org-top-card-module__name mb1 Sans-26px-black-85%-light"]').text.encode("utf-8")
            #print tmp['Name']
        except:
            return
        try:
            tmp['linkedinUrlId'] = url
            tmp['linkedinId'] = url.split('/')[-1]
        except:
            pass
        try:
            tmp['description'] = browser.find_element_by_xpath('//p[@class="org-about-us-organization-description__text description mb5 pre-wrap Sans-15px-black-70%"]').text.encode("utf-8")
        except:
            pass
        try:
            tmp['specialties'] = browser.find_elements_by_xpath('//p[@class="org-about-company-module__specialities mb5 Sans-15px-black-70%"]').text.encode('utf-8')
            #print tmp['Specialties']
        except:
            pass
        try:
            tmp['website'] = browser.find_element_by_xpath('//dd[@class="org-about-company-module__company-page-url Sans-15px-black-70%"]/a').text.encode("utf-8")
        except:
            pass
        try:
            tmp['employeeSizeRangeFrom'] = browser.find_element_by_xpath('//dd[@class="org-about-company-module__staff-count-range Sans-15px-black-70%"]').text.encode("utf-8")
        except:
            pass
        try:
            tmp['industry'] = browser.find_element_by_xpath('//dd[@class="org-about-company-module__industry Sans-15px-black-70%"]').text.encode("utf-8")
        except:
            pass
        try:
            tmp['founded'] = browser.find_element_by_xpath('//dd[@class="org-about-company-module__founded-year Sans-15px-black-70%"]').text.encode("utf-8")
        except:
            pass
        try:
            tmp['addressLocality'] = browser.find_element_by_xpath('//dd[@class="org-about-company-module__headquarter Sans-15px-black-70%"]').text.encode("utf-8")
        except:
            pass
        try:
            tmp['followers'] = int(''.join(browser.find_element_by_xpath('//p[@class="org-top-card-module__followers-count Sans-15px-black-55%"]').text.encode("utf-8").split(" f")[0].split(",")).strip())
        except:
            pass
        try:
            tmp['relatedPeople'] = browser.find_elements_by_xpath('//a[@class="org-company-employees-snackbar__details-highlight snackbar-description-see-all-link"]').get_attribute('href')
        except:
            pass
        try:
            tmp['affiliatedCompanies'] = []
            aff = browser.find_elements_by_xpath('//li[@class="companies-related-entities-list-item"]')
            for af in aff:
                tmp['affiliatedCompanies'].append(af.find_element_by_xpath('.//a[@class="company-name-link ember-view"]').get_attribute('href'))
        except:
            pass
        tmp['pageHtml'] = browser.page_source.encode('utf-8')
        tmp['status'] = {'status' : 2}
        return tmp
    
    try:
        tag = browser.find_element_by_xpath("//meta[@name='pageKey']").get_attribute('content')
    except:
        tag = ""
    print tag
    if tag == 'biz_companies_home_internal':
         return tag
    ##Only to be run locally
    if tag == 'uno-reg-join' or tag == 'uas-consumer-login-internal':
        return link
    ########################
    if tag == 'biz-company-login' or tag == 'biz-company-public' or tag == 'biz-showcase-login':
        try:
            browser.find_element_by_xpath('//button[@class="view-more-bar view-toggle-bar"]').click()
        except:
            pass
        tmp = {}
        try:
            tmp['name'] = browser.find_element_by_xpath('//h1[@class="name"]/span').text.encode("utf-8")
        except:
            return
        try:
            tmp['linkedinUrlId'] = url
            tmp['linkedinId'] = url.split('/')[-1]
        except:
            pass
        try:
            tmp['description'] = browser.find_element_by_xpath('//div[@class="basic-info-description"]/p').text.encode("utf-8")
        except:
            pass
        try:
            tmp['specialties'] = browser.find_element_by_xpath('//div[@class="specialties"]/p').text.encode("utf-8")
        except:
            pass
        try:
            tmp['website'] = browser.find_element_by_xpath('//li[@class="website"]/p/a').text.encode("utf-8")
        except:
            pass
        try:
            tmp['employeeSizeRangeFrom'] = browser.find_element_by_xpath('//li[@class="company-size"]/p').text.encode("utf-8")
        except:
            pass
        try:
            tmp['industry'] = browser.find_element_by_xpath('//li[@class="industry"]/p').text.encode("utf-8")
        except:
            pass
        try:
            tmp['founded'] = browser.find_element_by_xpath('//li[@class="founded"]/p').text.encode("utf-8")
        except:
            pass
        try:
            tmp['streetAddress'] = browser.find_element_by_xpath('//span[@class="street-address"]').text.encode("utf-8")
        except:
            pass
        try:
            tmp['addressLocality'] = browser.find_element_by_xpath('//span[@class="locality"]').text.encode("utf-8")
        except:
            pass
        try:
            tmp['region'] = browser.find_element_by_xpath('//abbr[@class="region"]').text.encode("utf-8")
        except:
            pass
        try:
            tmp['postalCode'] = browser.find_element_by_xpath('//span[@class="postal-code"]').text.encode("utf-8")
        except:
            pass
        try:
            tmp['country'] = browser.find_element_by_xpath('//span[@class="country-name"]').text.encode("utf-8")
        except:
            pass
        try:
            #people =  browser.find_element_by_xpath('//a[@class="density"]').get_attribute('href')
            tmp['followers'] = int(''.join(browser.find_element_by_xpath('//p[@class="followers-count"]').text.encode("utf-8").split(" f")[0].split(",")).strip())
        except:
            pass
        try:
            tmp['relatedPeople'] = "https://www.linkedin.com/vsearch/p?f_CC=" + tmp['ID']
        except:
            pass
        try:
        	tmp['affiliatedCompanies'] = []
        	aff = browser.find_elements_by_xpath('//p[@class="affiliated-company-name"]')
        	for af in aff:
        		tmp['affiliatedCompanies'].append(af.find_element_by_xpath('.//a').get_attribute('href'))
        except:
        	pass
        tmp['pageHtml'] = browser.page_source.encode('utf-8')
        tmp['status'] = {'status' : 2}
        return tmp


def main():
    Display.start()
    #Connect to MongoInstance
    client = MongoClient('mongodb://ip:port')
    db = client.Linkedin
    coll = db.CompanyED
    c1 = db.VerifyThese
    browser = ''
    browser = login(browser)
    ##Status 4 corresponds to new Linkedin crawl test
    while(True):
		query = {'status.status':{'$ne' : 2}}
		count = coll.find(query).count()
		tmp = coll.find(query).limit(1).skip(randint(0,min(1000,count-1)))
		try:
			tmp = tmp.next()
		except:
			break
		rnd = randint(0,4)
		#print rnd
		#if rnd == 2:
		#browser = new_login(browser)
		if tmp == None:
			break
		data = get_data(tmp['linkedinUrlId'], browser)
		#print data
		if data == 'biz_companies_home_internal':
			coll.remove({'_id':tmp['_id']})
			continue
		if data == tmp['linkedinUrlId']:
			#c2.insert({'linkedinUrlId':data})
			print '---------------------------'
			continue
		if data:
			print "Update"
			data['fetchedBy'] = 'Ayush' #Ayush,Surbhi,Anupam,Avidan: put your name to keep track
			data['lastModified'] = datetime.utcnow()
			coll.update({'_id':tmp['_id']},{'$set':data})
	        time.sleep(3)	
    try:
        browser.quit()
    except:
        pass
	Display.stop()


if __name__ == '__main__':
	main()
