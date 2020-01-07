from selenium import webdriver

browser = webdriver.Firefox()
browser.get('https://www.flashscore.com/basketball/europe/euroleague/')

while 1:
	print(browser.page_source)