"""
Creator: Michael Thane
Last Revised: 3/4/2019
Description: This library contains any and all functions used throughout this application.
             This will improve readability and organization.
"""
import bs4
import pandas as pd


# Determine if string is a number
def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


# Get list of values indicated by analyzingValue.
# When using isNumber(), remove unicode in string.
def getValues(analyzingValue, tags):
    returnList = []
    returnSet = set()
    for elem in tags:
        correctRow = 0
        subTags = elem.select('td')
        for data in subTags:
            ### Clean string to raw value
            # Check if the table data text equals the requested value
            if data.text.strip('\n') == analyzingValue and data.text.strip('\n') not in returnSet:
                correctRow = 1
                returnList.append(data.text.strip('\n'))
                returnSet.add(data.text.strip('\n'))
            if isNumber(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', '')
                            .replace(u'\xa0', '')) \
                    and isNumber(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', '')
                                     .replace(u'\xa0', '')) not in returnSet\
                    and correctRow == 1:
                returnList.append(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', '')
                                  .replace(u'\xa0', ''))
                returnSet.add(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', '')
                                  .replace(u'\xa0', ''))
    return returnList


# Parse a single 10k for desired values.
def parse10k(filePath):

    soup = bs4.BeautifulSoup(open(filePath), 'html.parser')

    attributeList = soup.select('tr')

    liabilities = getValues("Total liabilities", attributeList)
    assets = getValues("Total assets", attributeList)
    debt = getValues("Long-term debt", attributeList)
    equity = getValues("Total stockholders’ equity", attributeList)
    dilutedEPS = getValues("Diluted earnings per share", attributeList)
    dividends = getValues("Common stock cash dividends paid", attributeList)
    netIncome = getValues("Net income", attributeList)
    totalRevenue = getValues("Total revenue", attributeList)
    retainedEarnings = getValues("Retained earnings", attributeList)

    # print(liabilities)
    # print(assets)
    # print(debt)
    # print(equity)
    # print(dilutedEPS)
    # print(dividends)
    # print(netIncome)
    # print(totalRevenue)
    # print(retainedEarnings)
    # print()
    # pprint(getValues("Year Ended June 30,", attributeList))

    listOfLists = [liabilities,
                   assets,
                   debt,
                   equity,
                   dilutedEPS,
                   dividends,
                   netIncome,
                   totalRevenue,
                   retainedEarnings]

    longestLen = 0
    for thisList in listOfLists:
        if len(thisList[1:]) > longestLen:
            longestLen = len(thisList[1:])

    for thisList in listOfLists:
        if len(thisList[1:]) < longestLen:
            for i in range(longestLen - len(thisList[1:])):
                thisList.append(0)

    valueDict = {}
    for thisList in listOfLists:
        valueDict[thisList[0]] = thisList[1:]

    # print(valueDict)

    df = pd.DataFrame(data=valueDict)

    pd.set_option('display.max_columns', 20)

    return df
