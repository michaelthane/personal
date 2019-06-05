import AllFunctions as af
import os
import bs4
import time
import pandas as pd
from collections import OrderedDict


# Create list of file names in directory.

# for filename in os.listdir('Companies/MSFT'):
#     filePath = 'Companies/MSFT' + '/' + filename
#     print('Companies/MSFT' + '/' + filename)

# print(af.parse10k('Companies/MSFT/msft-10k_20180630.htm'))
# print(af.parse10k('Companies/MSFT/msft-10k_20170630.htm'))


# implement code to look for page break
# only start recording when on balance sheets page, reset when new page break occurs

# check if line if a<>
# print(open('Companies/MSFT/msft-10k_20180630.htm').read())

# msft = open('Companies/MSFT/msft-10k_20180630.htm')
# example = open('example3.html')
#
# # data is an array. Must convert to string to pass into BeautifulSoup.
# data = example.readlines()
#
# example.close()

# .join() concatenates each elem of an iterable to the string and returns the concatenated string.
#soup = bs4.BeautifulSoup("".join(data), features='lxml')
# soup = bs4.BeautifulSoup(open('example3.html'), 'html.parser')
#
# # Print ONLY the strings (without whitespace) from the descendants...
# pos = 0
# table = dict()
# col_names = []
# exclusions = ["millions", "$"]  # list of strings to be excluded
# for elem in soup.stripped_strings:
#
#     # Starting with the date, the first row will be the col names, except for the unit (in millions) and '$'
#     if elem in exclusions:
#         continue  # Go to the next loop iteration
#
#     # First elem should be a date like 'June 30' or similar.
#     if pos == 0:
#         table[elem] = []  # key = elem : value = list
#         col_names.append(elem)
#         pos += 1
#
#     if af.isNumber(elem) and pos < 3:
#         # These elems should be years like '2018' or '2017' or similar.
#         table[elem] = []
#         col_names.append(elem)
#         pos += 1
#     elif not af.isNumber(elem) and pos >= 3:
#         # If it is not a number and not in exclusions list, it will ALWAYS go in the first column.
#         table.get(col_names[0]).append(elem)
#
#         # If an element has been added to a column out of order, fill remaining columns with hyphens.
#         if (pos % 3) != 0 and (len(table.get(col_names[0])) > len(table.get(col_names[1])) or
#                                len(table.get(col_names[0])) > len(table.get(col_names[2]))):
#             for i in range((len(table.get(col_names[0])) - len(table.get(col_names[1]))) - 1):
#                 table.get(col_names[1]).append("-")
#                 pos += 1
#
#             for i in range((len(table.get(col_names[0])) - len(table.get(col_names[2]))) - 1):
#                 table.get(col_names[2]).append("-")
#                 pos += 1
#         pos += 1
#     elif af.isNumber(elem) and pos > 3:
#         # Put financial value in appropriate position.
#         table.get(col_names[pos % 3]).append(elem)
#         pos += 1
#
# print(table)
# print(pd.DataFrame(data=table))

# print(af.decimate_page('example3.html'))

msft = open('Companies/MSFT/msft-10k_20180630.htm')
# print(example.readlines())

report = dict()
tags = ""
page_num = 0
start_time = time.time()
for line in msft:
    tags += line
    # If line starts with hr (horizontal row), store string and move to next page.
    if line[:4] == "<hr ":
        report["Page " + str(page_num)] = tags
        tags = ""
        page_num += 1
end_time = time.time()
print(end_time - start_time)
print()


# if any of the stripped strings equals index or table of contens or the like, store pages and numbers and break

table_of_contents = {}
chapter = ""

soup = bs4.BeautifulSoup(report.get("Page 1"), 'html.parser')

for elem in soup.stripped_strings:
    elem = elem.replace(u"\xa0", u" ")
    if af.isNumber(elem):
        table_of_contents[chapter] = int(elem)
        chapter = ""
    else:
        chapter += elem + " "
    # print(table_of_contents)
    # time.sleep(3)
table_of_contents.popitem()

# Get page numbers of Item 8 and such from the table of contents.
# print(pd.DataFrame(data=table_of_contents, index=[0]).transpose())
# print()

print(af.decimate_page(report.get("Page 53")))


