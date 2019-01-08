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

currentURL = browser.current_url

tempFile = urllib3.PoolManager()
res = tempFile.request('GET', currentURL)
soup = bs4.BeautifulSoup(res,'html.parser')
for link in soup.findAll('a'):
    print(link)
    print(link.get('href'))
# soup = bs4.BeautifulSoup(tempFile)


#
# testvar = browser.find_elements_by_tag_name("td")
# for i in range(len(testvar)):
#     print(i)
#     print(testvar[i].get_attribute("href"))
    # try:
    #     print(testvar[i].tag_name)
    #     print("success")
    # except "selenium.common.exceptions.StaleElementReferenceException":
    #     print('yikes')
    #     # "selenium.common.exceptions.StaleElementReferenceException"



#print(testvar[0].find_element_by_css_selector('a'))
#print(testvar)
# for i in range(len(testvar)):
#     print(i)
    # print(testvar[i].get_attribute('href'))
    # print(testvar[i].find_element_by_css_selector('a'))

    # testvar[i].find_element(
# testvar = browser.find_element_by_tag_name('td').get_attribute('nowrap')




# documentTable = browser.find_element_by_class_name('tableFile2')
# aelements = documentTable.findall

# htmlFile = documentTable.

# documentElements = browser.find_element_by_id('documentsbutton')
# documentElements.
# print(documentElements.click())
# documentElements.click()
# for i in range(len(documentElements)):
    # print(documentElements[i].get_attribute())

# documentButton.click()


# documentElements = browser.find_elements_by_tag_name('a')
# documentButtonList = []
# for i in range(len(documentElements)):
#     print(documentElements[i])
#     # if documentElements[i].('id') == 'documentsbutton':
#     #    documentButtonList.append(documentElements[i])
# documentElements[0].click()
#documentButtonList[0].click()
