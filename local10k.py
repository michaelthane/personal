import bs4
from pprint import pprint
import time

def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# Get list of values indicated by analyzingValue
def getValues(analyzingValue, tags):
    returnList = []
    for elem in tags:
        correctRow = 0
        subTags = elem.select('td')
        for data in subTags:
            ### Clean string to raw value
            # Check if the table data text equals the requested value
            if data.text.strip('\n') == analyzingValue:
                correctRow = 1
                returnList.append(data.text.strip('\n'))
            if isNumber(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', '')) \
                    and correctRow == 1:
                returnList.append(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', ''))
    return returnList


file = open('Companies/MSFT/msft-10k_20180630.htm')
exampleFile = open('example.html')

soup = bs4.BeautifulSoup(file, 'html.parser')

attributeList = soup.select('tr')

print(getValues("Total liabilities", attributeList))
print(getValues("Total assets", attributeList))
print(getValues("Long-term debt", attributeList))
print(getValues("Total stockholders’ equity", attributeList))
print(getValues("Diluted earnings per share", attributeList))
print(getValues("Common stock cash dividends paid", attributeList))
print(getValues("Net income", attributeList))
print(getValues("Total revenue", attributeList))
print(getValues("Retained earnings", attributeList))
print()
pprint(getValues("Year Ended June 30,", attributeList))

# If it starts with \xa0\xa0, remove it from list.
# If value is already in list, delete it, else, keep it.


# implement code to look for page break
# only start recording when on balance sheets page, reset when new page break occurs


# returnList = []
# reportValue = 'Total liabilities'
# for elem in attributeList:
#     correctRow = 0
#     data = elem.select('td')
#     for things in data:
#         if things.text.strip('\n') == reportValue:
#             correctRow = 1
#             returnList.append(things.text.strip('\n'))
#             # print(things.text.strip('\n'))
#         if isNumber(things.text.replace(',', '')) and correctRow == 1:
#             returnList.append(things.text.replace(',', ''))
#             #print(things.text.replace(',', ''))
# print(len(attributeList))



