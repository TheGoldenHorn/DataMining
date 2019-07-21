################################################################################
#   ALEXA Crawling Script                                                      #
#	Written By : Ayush                                                         #
################################################################################

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


def main():
	profile = webdriver.FirefoxProfile()
	profile.set_preference('permissions.default.stylesheet', 2)
	profile.set_preference('permissions.default.image', 2)
	profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
	profile.update_preferences()
	browser = webdriver.Firefox(firefox_profile=profile)
	#browser = webdriver.Firefox()

	#Get Site
	#browser.implicitly_wait(10)
	browser.get('http://www.alexa.com/siteinfo/amazon.com')
	time.sleep(5)
	
	#Input the website to be searched
	#elt = browser.find_element_by_xpath('.//input[@id="siteInput"]')
	#elt.send_keys('amazon.com')
	#time.sleep(2)

	#Click the find button
	#elt = browser.find_element_by_xpath('.//a[@class="Button Mkbutton Darkblue"]')
	#elt.click()
	#time.sleep(3)

	#Alexa traffic ranks
	print 'Global Rank ' + browser.find_element_by_xpath('.//strong[@class="metrics-data align-vmiddle"]').text
	print 'Rank Stat ' + browser.find_element_by_xpath('.//span[@class="align-vmiddle change-wrapper change-up change-r2"]').get_attribute('title')

	countryRank = browser.find_element_by_xpath('.//span[@data-cat="countryRank"]')
	print countryRank.find_element_by_xpath('.//h4').text + " " + countryRank.find_element_by_xpath('.//strong[@class="metrics-data align-vmiddle"]').text

	#country table
	table = browser.find_element_by_xpath('.//table[@id="demographics_div_country_table"]')
	for link in table.find_elements_by_xpath('.//tr[@class=" "]'):
		print link.text


	#how engaged visitors are
	visitors = browser.find_element_by_xpath('.//section[@id="engagement-content"]')

	for link in visitors.find_elements_by_xpath('.//span[@class="span4"]'):
		#print link
		try:
			print link.find_element_by_xpath('.//h4[@class="metrics-title"]').text
			print link.find_element_by_xpath('.//strong[@class="metrics-data align-vmiddle"]').text
		except:
			pass

		try:
			print link.find_element_by_xpath('.//span[@class="align-vmiddle change-wrapper change-down color-gen2 "]').get_attribute('title')
		except:
			pass
		try:		
			print link.find_element_by_xpath('.//span[@class="align-vmiddle change-wrapper change-up change-r"]').get_attribute('title')
		except:
			pass	

	#search traffic
	traffic = browser.find_element_by_xpath('.//section[@id="keyword-content"]')
	print traffic.find_element_by_xpath('.//strong[@class="metrics-data align-vmiddle"]').text
	print traffic.find_element_by_xpath('.//span[@data-cat="search_percent"]').text #percentage up or down??? 
	#print traffic.find_element_by_xpath('.//span[@data-cat="search_percent"]').get_attribute('title')  #no output

	#Keywords
	keywords = browser.find_element_by_xpath('.//table[@id="keywords_top_keywords_table"]')
	for link in keywords.find_elements_by_xpath('.//tr[@class=" "]'):
		print link.text

	#upstream sites
	upstream = browser.find_element_by_xpath('.//table[@id="keywords_upstream_site_table"]')
	for link in upstream.find_elements_by_xpath('.//tr[@class=" "]'):
		print link.text

	siteLinks = browser.find_element_by_xpath('.//section[@id="linksin-panel-content"]')
	print siteLinks.find_element_by_xpath('.//span[@class="font-4 box1-r"]').text
	for link in siteLinks.find_elements_by_xpath('.//tr[@class=" "]'):
		print link.find_element_by_xpath('.//td[@class=""]').text
		print link.find_element_by_xpath('.//a[@class="word-wrap"]').get_attribute('href')

	#sites related
	sitesRelated = browser.find_element_by_xpath('.//table[@id="audience_overlap_table"]')
	for link in sitesRelated.find_elements_by_xpath('.//tr[@class=" "]'):
		print link.text	

	sitesOwned = browser.find_element_by_xpath('.//table[@id="owned_link_table"]')
	for link in sitesOwned.find_elements_by_xpath('.//tr[@class=" "]'):
		print link.find_element_by_xpath('.//a').get_attribute('href')


	#subdomains
	subdomain = browser.find_element_by_xpath('.//table[@id="subdomain_table"]')
	for link in subdomain.find_elements_by_xpath('.//tr[@class=" "]'):
		print link.text

	#laoding speed
	speed = browser.find_element_by_xpath('.//section[@id="loadspeed-panel"]')
	print speed.text


	summary = browser.find_element_by_xpath('.//section[@id="contact-panel-content"]')
	print summary.find_element_by_xpath('.//p').text
	print summary.find_element_by_xpath('.//p[@class="color-s3"]').text

	#who visits
	'''gender = browser.find_element_by_xpath('.//div[@class="row-fluid col-pad pybar demo-gender"]')
	sGender= gender.find_element_by_xpath('.//div[@class="row-fluid pybar-row"]')
	subgender = sGender.find_elements_by_xpath('.//span[@class="pybar-bars"]')
	#for link in subgender.find_elements_by_xpath('.//span[@class="container"]'):
	for link in subgender:
		print link.text'''

	#Categories with related sites
	categoryTable = browser.find_element_by_xpath('.//table[@id="category_link_table"]')
	for links in categoryTable.find_elements_by_xpath('.//span[@class=""]/a'):
		
			print links.get_attribute('href')


	

	raw_input()
	return

if __name__ == '__main__':
	main()
