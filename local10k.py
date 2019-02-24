import bs4
from pprint import pprint
import time

def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def getValues(analyzingValue, tags):
    returnList = []
    for elem in tags:
        correctRow = 0
        subTags = elem.select('td')
        for data in subTags:
            if data.text.strip('\n') == analyzingValue:
                correctRow = 1
                returnList.append(data.text.strip('\n'))
                # print(things.text.strip('\n'))
            if isNumber(data.text.replace(',', '')) and correctRow == 1:
                returnList.append(data.text.strip('\n').replace(',', ''))
                # print(things.text.replace(',', ''))
    return returnList


file = open('Companies/MSFT/msft-10k_20180630.htm')
exampleFile = open('example.html')

soup = bs4.BeautifulSoup(file, 'html.parser')

attributeList = soup.select('tr')

print(getValues('Total liabilities', attributeList))

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



