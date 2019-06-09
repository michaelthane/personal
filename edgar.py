import AllFunctions as af
from selenium import webdriver
import bs4
import urllib3
from urllib.request import *
import fnmatch
import time
import requests

# Initialize
ticker = 'msft'
filing = '10-k'


# browser = webdriver.Chrome("C:/Users/h217023/Desktop/Michael's Stuff/pycharm/projects/venv/Lib/site-packages/selenium/webdriver/chrome")

# Begin session
browser = webdriver.Chrome()

# Open browser
browser.get('https://www.sec.gov')

# Navigate to given company and filing.
companyName = browser.find_element_by_id('company-name')
companyName.send_keys(ticker)
tickerSearchButton = browser.find_element_by_id('edgar-search-button')
tickerSearchButton.click()
filingType = browser.find_element_by_name('type')
filingType.send_keys(filing)
inputElements = browser.find_elements_by_tag_name('input')

for i in range(len(inputElements)):

    if inputElements[i].get_attribute('type') == 'submit' and inputElements[i].get_attribute('value') == 'Search':
        filingSearchButton = inputElements[i]

filingSearchButton.click()

http = urllib3.PoolManager()

time.sleep(0.5)

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

# html = urlopen(browser.current_url)
# print(html.read())
# with open("Companies/storage.html", "w") as f:
#     f.write(html.read())

time.sleep(1)

# STARTING LINE
soup3 = bs4.BeautifulSoup(response3.data, features="lxml")

# At this point, soup3 is the "html file" you need.

start = time.time()

temp = af.create_pages(soup3)

print("DONE" + "\n")

print(af.dict_to_df(temp, transpose=True))
print()

print("Execution time: " + str(time.time() - start))
print()

toc = af.get_table_of_contents(temp)
print(af.dict_to_df(toc, transpose=True))
print()

pn = af.get_page_num(temp, toc)
print("Item 8 is page number: " +str(pn))
print()

statement = af.decimate_page(temp.get("Page " + str(pn)))
print(af.dict_to_df(statement))


# with open("Companies/storage.html", "w") as f:
#     f.write(str(soup3.find_all()))
# HHTPResponse.data -> bytes
"""
soup3 = bs4.BeautifulSoup(response3.data, features="lxml")

# At this point, soup3 is the "html file" you need.

start = time.time()

temp = af.create_pages(soup3)

print("DONE" + "\n")

# print(af.dict_to_df(temp, transpose=True))

print()

print("Execution time: " + str(time.time() - start))

income_statements = []
balance_statements = []
cash_flow_statements = []
equity_statements = []

income_combo = {}
balance_combo = {}
cash_flow_combo = {}
equity_combo = {}

report = af.create_pages(soup3)

toc = af.get_table_of_contents(report)
pn = af.get_page_num(report, toc)

# Assume that pn + 1 is comprehensive income statement
# if its not there add 1, 2, 3 respectively instead.
pn_income = pn
pn_balance = pn + 2
pn_cash_flow = pn + 3
pn_equity = pn + 4

income_statement = af.decimate_page(report.get("Page " + str(pn_income)))
balance_statement = af.decimate_page(report.get("Page " + str(pn_balance)))
cash_flow_statement = af.decimate_page(report.get("Page " + str(pn_cash_flow)))
equity_statement = af.decimate_page(report.get("Page " + str(pn_equity)))

income_statements.append(income_statement)
balance_statements.append(balance_statement)
cash_flow_statements.append(cash_flow_statement)
equity_statements.append(equity_statement)

# INCOME
if len(income_statements) == 2:
    income_combo = af.combine_statements(income_statements[0], income_statements[1])
    # print("\n" + "COMBO COMING" + "\n")
    # print(af.dict_to_df(income_combo))
elif len(income_statements) > 2:
    income_combo = af.combine_statements(income_combo, income_statements[-1])
    # print("\n" + "COMBO COMING" + "\n")
    # print(af.dict_to_df(income_combo))
else:
    pass

# BALANCE
if len(balance_statements) == 2:
    balance_combo = af.combine_statements(balance_statements[0], balance_statements[1])
    # print("\n" + "COMBO COMING" + "\n")
    # print(af.dict_to_df(balance_combo))
elif len(balance_statements) > 2:
    balance_combo = af.combine_statements(balance_combo, balance_statements[-1])
    # print("\n" + "COMBO COMING" + "\n")
    # print(af.dict_to_df(balance_combo))
else:
    pass

# CASH FLOW
if len(cash_flow_statements) == 2:
    cash_flow_combo = af.combine_statements(cash_flow_statements[0], cash_flow_statements[1])
    # print("\n" + "COMBO COMING" + "\n")
    # print(af.dict_to_df(cash_flow_combo))
elif len(cash_flow_statements) > 2:
    cash_flow_combo = af.combine_statements(cash_flow_combo, cash_flow_statements[-1])
    # print("\n" + "COMBO COMING" + "\n")
    # print(af.dict_to_df(cash_flow_combo))
else:
    pass

# EQUITY
if len(equity_statements) == 2:
    equity_combo = af.combine_statements(equity_statements[0], equity_statements[1])
    # print("\n" + "COMBO COMING" + "\n")
    # print(af.dict_to_df(equity_combo))
elif len(equity_statements) > 2:
    equity_combo = af.combine_statements(equity_combo, equity_statements[-1])
    # print("\n" + "COMBO COMING" + "\n")
    # print(af.dict_to_df(equity_combo))
else:
    pass


print()
print("INCOME")
print()
print(af.dict_to_df(income_statement))
print()
print("BALANCE SHEET")
print()
print(af.dict_to_df(balance_statement))
print()
print("CASH FLOW")
print()
print(af.dict_to_df(cash_flow_statement))
print()
print("EQUITY")
print()
print(af.dict_to_df(equity_statement))
print()
print("Execution time: " + str(time.time() - start))




# for fragment in soup3.findAll('a'):
#
#     if fragment.get("href") == "#ITEM_8_FINANCIAL_STATEMENTS_AND_SUPPLEM":
#         print(fragment)
#         print(fragment.get("href"))
#         var = fragment.get("href")
#         break
#     else:
#         continue
#
# browser.get(browser.current_url + var)
#
# time.sleep(1)
#
# response4 = http.request('GET', browser.current_url)
#
# soup4 = bs4.BeautifulSoup(response4.data, features="lxml")
#
# for fragment in soup4.findAll('hr'):
#     print(fragment)

# append tags into list until a page break is observed
"""
