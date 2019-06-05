"""
Creator: Michael Thane
Last Revised: 3/4/2019
Description: This library contains any and all functions used throughout this application.
             This will improve readability and organization.
"""
import bs4
import os
import pandas as pd


# Determine if string is a number
def isNumber(string):
    exclusions = [',', '$']
    try:
        float(string.replace(',', ''))
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

    # The strings are hardcoded for this specific company.
    # Future work must make it possible for ANY company.
    liabilities      = getValues("Total liabilities", attributeList)
    assets           = getValues("Total assets", attributeList)
    debt             = getValues("Long-term debt", attributeList)
    equity           = getValues("Total stockholders’ equity", attributeList)
    dilutedEPS       = getValues("Diluted earnings per share", attributeList)
    dividends        = getValues("Common stock cash dividends paid", attributeList)
    netIncome        = getValues("Net income", attributeList)
    totalRevenue     = getValues("Total revenue", attributeList)
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

    # Find finance that has the most elements.
    longestLen = 0
    for thisList in listOfLists:
        if len(thisList[1:]) > longestLen:
            longestLen = len(thisList[1:])

    # Add zeros for finances that have less than the max.
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


# Return a dataframe of the financial data at file path.
# Probably call this separately for table...
def decimate_page(file_path, table={}, col_names=[]):

    if len(file_path) < 260:  # MAX_PATH length
        soup = bs4.BeautifulSoup(open(file_path), 'html.parser')
    else:
        soup = bs4.BeautifulSoup(file_path, 'html.parser')

    # Print ONLY the strings (without whitespace) from the descendants...
    pos = 0
    # table = {}
    # col_names = []
    exclusions = ["millions", "$", "PART II", "Item 8"]  # list of strings to be excluded
    for elem in soup.stripped_strings:

        # Starting with the date, the first row will be the col names, except for the unit (in millions) and '$'
        if elem in exclusions:
            continue  # Go to the next loop iteration

        # First elem should be a date like 'June 30' or similar.
        if pos == 0:
            table[elem] = []  # key = elem : value = list
            col_names.append(elem)
            pos += 1

        if isNumber(elem) and pos < 3:
            # These elems should be years like '2018' or '2017' or similar.
            table[elem] = []
            col_names.append(elem)
            pos += 1
        #elif (elem[0] == "$" or elem[:3] == "and") and len(elem) > 1:
        #    # If description column has numeric values, include them in description.
        #    table.get(col_names[0])[-1] += elem
        elif not isNumber(elem) and pos >= 3:
            # If it is not a number and not in exclusions list, it will ALWAYS go in the first column.
            table.get(col_names[0]).append(elem)

            # If an element has been added to a column out of order, fill remaining columns with hyphens.
            if (pos % 3) != 0 and (len(table.get(col_names[0])) > len(table.get(col_names[1])) or
                                   len(table.get(col_names[0])) > len(table.get(col_names[2]))):
                for i in range((len(table.get(col_names[0])) - len(table.get(col_names[1]))) - 1):
                    table.get(col_names[1]).append("-")
                    pos += 1

                for i in range((len(table.get(col_names[0])) - len(table.get(col_names[2]))) - 1):
                    table.get(col_names[2]).append("-")
                    pos += 1
            pos += 1
        elif isNumber(elem) and pos > 3:
            # Put financial value in appropriate position.
            table.get(col_names[pos % 3]).append(elem)
            pos += 1

    if len(table.get(col_names[0])) > len(table.get(col_names[1])):
        for i in range((len(table.get(col_names[0])) - len(table.get(col_names[1])))):
            table.get(col_names[1]).append("-")
    if len(table.get(col_names[0])) > len(table.get(col_names[2])):
        for i in range((len(table.get(col_names[0])) - len(table.get(col_names[2])))):
            table.get(col_names[2]).append("-")

    return pd.DataFrame(data=table)


"""
End of file.
"""
