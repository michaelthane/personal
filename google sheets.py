from selenium import webdriver
import bs4
import urllib3
import fnmatch
import time

browser = webdriver.Chrome()
browser.get('https://accounts.google.com/signin/v2/identifier?service=wise&passive=1209600&continue=https%3A%2F%2Fdocs'
            '.google.com%2Fspreadsheets%2F%3Fusp%3Dmkt_sheets&followup=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2F'
            '%3Fusp%3Dmkt_sheets&ltmpl=sheets&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

inputs = browser.find_elements_by_tag_name('input')
email = 'mthane96@gmail.com'

emailField = browser.find_element_by_name('identifier')
emailField.send_keys(email)

# for element in inputs:
#     if element.get_attribute('type') == 'email':
#         element.send_keys(email)

nextButton = browser.find_element_by_id('identifierNext')
nextButton.click()

time.sleep(1.0)  # sleep to allow new page elements to populate

password = 'mt511217'

passwordField = browser.find_element_by_name('password')
passwordField.send_keys(password)

nextButton = browser.find_element_by_id('passwordNext')
nextButton.click()



# companyName = browser.find_element_by_id('company-name')
# # ticker = input('Enter ticker: ')
# ticker = 'msft'
# companyName.send_keys(ticker)
#
# tickerSearchButton = browser.find_element_by_id('edgar-search-button')
# tickerSearchButton.click()
#
# filingType = browser.find_element_by_name('type')
# # filing = input('Enter filing type: ')
# filing = '10-k'
# filingType.send_keys(filing)
#
# inputElements = browser.find_elements_by_tag_name('input')
#
# for i in range(len(inputElements)):
#
#     if inputElements[i].get_attribute('type') == 'submit' and inputElements[i].get_attribute('value') == 'Search':
#         filingSearchButton = inputElements[i]
#
# filingSearchButton.click()
#
# http = urllib3.PoolManager()
#
# time.sleep(0.1)
#
# response = http.request('GET', browser.current_url)
#
# soup = bs4.BeautifulSoup(response.data, features="lxml")
# list1 = []
# list2 = []
# for link in soup.findAll('a'):
#     list1.append(link.get("href"))
#     # print(link.get("href"))
#
# list2 = fnmatch.filter(list1, '/Archives/*')
#
# for i in list2:
#     print(i)
#
# firstLink = list2[0]
#
# browser.get("https://www.sec.gov" + firstLink)
#
# ### Do it again.
#
# time.sleep(0.1)
#
# response2 = http.request('GET', browser.current_url)
#
# soup2 = bs4.BeautifulSoup(response2.data, features="lxml")
# list3 = []
# list4 = []
# for link in soup2.findAll('a'):
#     list3.append(link.get("href"))
#     print(link.get("href"))
#
# list4 = fnmatch.filter(list3, '/Archives/*')
#
# print("list4: ")
# for i in list4:
#     print(i)
#
# firstLink = list4[0]
#
# browser.get("https://www.sec.gov" + firstLink)
