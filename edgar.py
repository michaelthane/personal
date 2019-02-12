from selenium import webdriver
import bs4
import urllib3
import urllib

browser = webdriver.Chrome()
browser.get('https://www.sec.gov')

companyName = browser.find_element_by_id('company-name')
# ticker = input('Enter ticker: ')
ticker = 'msft'
companyName.send_keys(ticker)

tickerSearchButton = browser.find_element_by_id('edgar-search-button')
tickerSearchButton.click()

filingType = browser.find_element_by_name('type')
# filing = input('Enter filing type: ')
filing = '10-k'
filingType.send_keys(filing)

inputElements = browser.find_elements_by_tag_name('input')
# list1 = inputElements.get_attribute('type')


for i in range(len(inputElements)):

    if inputElements[i].get_attribute('type') == 'submit' and inputElements[i].get_attribute('value') == 'Search':
        filingSearchButton = inputElements[i]

filingSearchButton.click()

# tableFile = browser.find_element_by_class_name('tableFile2')


# This only works sometimes where the address will print out
alpha = browser.find_element_by_partial_link_text('Documents')
browser.get(alpha.get_attribute('href'))

# address = alpha.get_attribute('href')
# print(address)
