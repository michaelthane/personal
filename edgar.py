from selenium import webdriver
import bs4
import urllib3
import fnmatch
import time
import AllFunctions as af


browser = webdriver.Chrome("C:/Users/h217023/Desktop/Michael's Stuff/pycharm/projects/venv/Lib/site-packages/selenium/webdriver/chrome")
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

for i in range(len(inputElements)):

    if inputElements[i].get_attribute('type') == 'submit' and inputElements[i].get_attribute('value') == 'Search':
        filingSearchButton = inputElements[i]

filingSearchButton.click()

http = urllib3.PoolManager()

time.sleep(0.1)

response = http.request('GET', browser.current_url)

soup = bs4.BeautifulSoup(response.data, features="lxml")
list1 = []
list2 = []
for link in soup.findAll('a'):
    list1.append(link.get("href"))
    # print(link.get("href"))

list2 = fnmatch.filter(list1, '/Archives/*')

for i in list2:
    pass
    # print(i)

firstLink = list2[0]

browser.get("https://www.sec.gov" + firstLink)

### Do it again.

time.sleep(0.1)

response2 = http.request('GET', browser.current_url)

soup2 = bs4.BeautifulSoup(response2.data, features="lxml")
list3 = []
list4 = []
for link in soup2.findAll('a'):
    list3.append(link.get("href"))
    # print(link.get("href"))

list4 = fnmatch.filter(list3, '/Archives/*')

# print("list4: ")
# for i in list4:
#     print(i)

firstLink = list4[0]

browser.get("https://www.sec.gov" + firstLink)

time.sleep(1)

response3 = http.request('GET', browser.current_url)

soup3 = bs4.BeautifulSoup(response3.data, features="lxml")

for fragment in soup3.findAll('a'):

    if fragment.get("href") == "#ITEM_8_FINANCIAL_STATEMENTS_AND_SUPPLEM":
        print(fragment)
        print(fragment.get("href"))
        var = fragment.get("href")
        break
    else:
        continue

browser.get(browser.current_url + var)

time.sleep(1)

response4 = http.request('GET', browser.current_url)

soup4 = bs4.BeautifulSoup(response4.data, features="lxml")

for fragment in soup4.findAll('a'):
    print(fragment)
