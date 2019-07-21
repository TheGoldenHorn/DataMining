from selenium import webdriver
from pymongo import MongoClient
from random import random
import time, sys, re
from datetime import datetime
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
Display = Display(visible=0, size=(800, 600))
Display.start()
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

client = MongoClient('mongodb://IP:PORT')
db = client.Linkedin

def login(browser):
    try:
        browser.quit()
    except:
        pass
    #binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
    #browser = webdriver.Firefox(firefox_binary=binary)
    browser = webdriver.Firefox()
    browser.get('http://app.avention.com')
    user = browser.find_element_by_id('username')
    user.send_keys('USERNAME')
    password = browser.find_element_by_id('password')
    password.send_keys('avention1')
    password.send_keys(u'\ue007')
    time.sleep(5)
    return browser


def norm_str(str):
    str = re.findall(r"[\w']+", str)
    stop_word = {'a' : '', 'and' : '', 'the' : '', 'private' : '', 'pvt' : '', 'limited' : '', 'ltd' : '',\
                 'inclusive' : '', 'inc' : '', 'group' : '', 'of' : '', 'corporation' : '', 'corp' : '',\
                 'corporate' : '', 'company' : '', 'comp' : '', 'systems' : '', 'system' : '', 'sys' : '',\
                 'service' : '', 'engineering' : '', 'eng' : '', 'llc' : '', 'association' : '', 'assoc' : '', \
                  'brothers' : '', 'bros' : '', 'co' : '', 'com' : '', 'manufacturing' : '', 'mfg' : '', \
                 'manufacturers' : '', 'mfrs' : ''}
    res = ''
    for word in str:
        word = word.lower()
        if word not in stop_word:
            res = res + word
            res = res + ' '
    return res

browser = ''
browser = login(browser)
#browser.implicitly_wait(10)
elt = browser.find_element_by_xpath('.//input[@id="search"]')
cursor = db.CompanyED.find({'isAventionSearchComplete' : {'$exists' : False}}, no_cursor_timeout = True)
for doc in cursor:
    #print doc
    #print doc['Name']
    match, zombie, contact = [], [], []
    try:
        find = db.AventionZombie.find({'name' : doc['name']})
    except:
        continue
    if find.count() != 0:
    	try:
    		db.LinkedinAventionMatch.insert\
    		({'name' : doc['name'], 'EDId' : doc['_id'], 'aventionMatch' : list(find), 'lastModified' : datetime.utcnow()})
    	except:
    		pass
        db.CompanyED.update({'_id' : doc['_id']}, {'$set' : {'isAventionSearchComplete' : True, 'lastModified' : datetime.utcnow()}})
        continue
    name = norm_str(doc['name']) #doc['Name'].split()
    print name
    found = False
    elt.clear()
    for wrd in name.split():
        #print wrd
        elt.send_keys(wrd)
        elt.send_keys(' ')
        time.sleep(random())
        try:
            out_block = WebDriverWait(browser, 2).until\
            (EC.presence_of_element_located((By.XPATH, './/div[@class="search-typeahead open"]/ul[@class="typeAheadMenu"]')))
            #out_block = browser.find_element_by_xpath('.//div[@class="search-typeahead open"]/ul[@class="typeAheadMenu"]')
        except:
            #print 'not detected outer block'
            break
        #Extract Suggestion
        for idx in xrange(1, 6):
            try:
                in_block = out_block.find_element_by_xpath('.//div[@class="company" and position()={pos}]/a'.format(pos=str(idx)))
                in_div = in_block.find_element_by_xpath('.//li/div[@class="query-name"]')
                link = in_block.get_attribute('href')
                comp_name = in_div.get_attribute('title')
                print 'matching', name, norm_str(comp_name)
                if norm_str(comp_name) == name:
                    match.append({'name' : comp_name, 'aventionUrl' : link})
                    print 'match found', doc['name'], comp_name
                    found = True
                else:
                    zombie.append({'name' : comp_name, 'aventionUrl' : link})
            except:
                break
        if idx == 5:
            idx = idx + 1
        # extract contacts from avention
        for jdx in xrange(idx, 11):
            try:
                in_block = out_block.find_element_by_xpath('.//div[@class="contact" and position()={pos}]/a'.format(pos=str(jdx)))
                in_div = in_block.find_element_by_xpath('.//li/div[@class="query-name"]')
                link = in_block.get_attribute('href')
                person = in_div.get_attribute('title')
                contact.append({'name' : person, 'aventionUrl' : link})
            except:
                #print 'not detected company contact'
                break
        if found:
            break
    if len(match) != 0:
        try:
            db.LinkedinAventionMatch.insert\
            ({'name' : doc['name'], 'EDId' : doc['_id'], 'aventionMatch' : match, 'lastModified' : datetime.utcnow()})
        except:
            pass
        db.CompanyED.update({'_id' : doc['_id']}, {'$set' : {'isAventionSearchComplete' : True, 'lastModified' : datetime.utcnow()}})
        #print doc['Name'], match
    else:
        db.CompanyED.update({'_id' : doc['_id']}, {'$set' : {'isAventionSearchComplete' : False, 'lastModified' : datetime.utcnow()}})
    if len(zombie) != 0:
        #print 'zombie', zombie
        for rec in zombie:
            rec.update({'EDId' : doc['_id'], 'lastModified' : datetime.utcnow()})
            try:
                db.AventionZombie.insert(rec)
            except:
                pass
    if len(contact) != 0:
        #print 'contact', contact
        for rec in contact:
            rec.update({'EDId' : doc['_id'], 'isContact' : True,'lastModified' : datetime.utcnow()})
            try:
                db.AventionZombie.insert(rec)
            except:
                pass
cursor.close()
Display.stop()

