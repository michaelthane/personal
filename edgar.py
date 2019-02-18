from selenium import webdriver
import bs4
import urllib3
import fnmatch

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

for i in range(len(inputElements)):

    if inputElements[i].get_attribute('type') == 'submit' and inputElements[i].get_attribute('value') == 'Search':
        filingSearchButton = inputElements[i]

filingSearchButton.click()

http = urllib3.PoolManager()

url = "https://www.sec.gov/cgi-bin/" \
      "browse-edgar?action=getcompany&CIK=0000789019&type=10-k&dateb=&owner=exclude&count=40"
response = http.request('GET', url)

soup = bs4.BeautifulSoup(response.data, features="lxml")
list1 = []
list2 = []
for link in soup.findAll('a'):
    list1.append(link.get("href"))
    # print(link.get("href"))

list2 = fnmatch.filter(list1, '/Archives/*')

for i in list2:
    print(i)

firstLink = list2[0]

browser.get("https://www.sec.gov" + firstLink)
