from selenium import webdriver

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

documentElements = browser.find_elements_by_id('documentsbutton')
for i in range(len(documentElements)):
    print(documentElements[i].get_attribute())

# documentButton.click()


# documentElements = browser.find_elements_by_tag_name('a')
# documentButtonList = []
# for i in range(len(documentElements)):
#     print(documentElements[i])
#     # if documentElements[i].('id') == 'documentsbutton':
#     #    documentButtonList.append(documentElements[i])
# documentElements[0].click()
#documentButtonList[0].click()
