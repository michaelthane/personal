import AllFunctions as af
import os
import bs4
import time
import pandas as pd
from dateutil.parser import parse
import re


# Create list of file names in directory.

# for filename in os.listdir('Companies/MSFT'):
#     filePath = 'Companies/MSFT' + '/' + filename
#     print('Companies/MSFT' + '/' + filename)

# print(af.parse10k('Companies/MSFT/msft-10k_20180630.htm'))
# print(af.parse10k('Companies/MSFT/msft-10k_20170630.htm'))


# implement code to look for page break
# only start recording when on balance sheets page, reset when new page break occurs

# soup = bs4.BeautifulSoup(open('Companies/MSFT/10-k.html'), 'html.parser')
#
# for elem in soup.tagStack:
#     print(elem)

"""
report1 = af.create_pages('Companies/MSFT/msft-10k_20180630.htm')
report2 = af.create_pages('Companies/MSFT/2017_10-k.html')
report3 = af.create_pages('Companies/MSFT/2016_10-k.html')
report4 = af.create_pages('Companies/MSFT/2015_10-k.html')
report5 = af.create_pages('Companies/MSFT/2014_10-k.html')
report6 = af.create_pages('Companies/MSFT/2013_10-k.html')

# print(af.dict_to_df(report2, transpose=True))

# report = af.create_pages('Companies/MSFT/d10k.htm')
# print(report)
# print(af.dict_to_df(report, transpose=True))
toc1 = af.get_table_of_contents(report1)
pn1 = af.get_page_num(report1, toc1)
# print(af.dict_to_df(toc1, transpose=True))
print()
toc2 = af.get_table_of_contents(report2)
pn2 = af.get_page_num(report2, toc2)
# print(af.dict_to_df(toc2, transpose=True))
print()
toc3 = af.get_table_of_contents(report3)
# print(af.dict_to_df(toc3, transpose=True))
# print()
# print(af.dict_to_df(report3, transpose=True))
pn3 = af.get_page_num(report3, toc3)
print("yeah yeet")

print()
toc4 = af.get_table_of_contents(report4)
pn4 = af.get_page_num(report4, toc4)
# print(af.dict_to_df(toc4, transpose=True))
print()
toc5 = af.get_table_of_contents(report5)
pn5 = af.get_page_num(report5, toc5)
# print(af.dict_to_df(toc4, transpose=True))
print()
toc6 = af.get_table_of_contents(report6)
pn6 = af.get_page_num(report6, toc6)
# print(af.dict_to_df(toc4, transpose=True))
print()
# Get page numbers of Item 8 and such from the table of contents.
# print(pd.DataFrame(data=table_of_contents, index=[0]).transpose())
# print()

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
statement1 = af.decimate_page(report1.get(pn1))
print(af.dict_to_df(statement1))
print()
print("NEXT STATEMENT")
print()
statement2 = af.decimate_page(report2.get(pn2))
print(af.dict_to_df(statement2))
print()
print("COMBO COMING")
print()
combo = af.combine_statements(statement1, statement2)
print(af.dict_to_df(combo))
print()
print("NEXT STATEMENT")
print()
statement3 = af.decimate_page(report3.get(pn3))
print(af.dict_to_df(statement3))
print()
print("COMBO COMING")
print()
combo = af.combine_statements(combo, statement3)
print(af.dict_to_df(combo))
print()
print("NEXT STATEMENT")
print()
statement4 = af.decimate_page(report4.get(pn4))
print(af.dict_to_df(statement4))
print()
print("COMBO COMING")
print()
combo = af.combine_statements(combo, statement4)
print(af.dict_to_df(combo))

print()
print("NEXT STATEMENT")
print()
statement5 = af.decimate_page(report5.get(pn5))
print(af.dict_to_df(statement5))
print()
print("COMBO COMING")
print()
combo = af.combine_statements(combo, statement5)
print(af.dict_to_df(combo))

print()
print("NEXT STATEMENT")
print()
statement6 = af.decimate_page(report6.get(pn6))
print(af.dict_to_df(statement6))
print()
print("COMBO COMING")
print()
combo = af.combine_statements(combo, statement6)
print(af.dict_to_df(combo))
# print(af.decimate_page(report.get("Page 51")))
# print(af.decimate_page(report.get("Page 52"), {}, []))
# print(af.decimate_page(report.get("Page 53")))
# print(af.decimate_page(report.get("Page 54")))
"""

start = time.time()

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

links = []
statements = []
combo = {}

links.append('Companies/MSFT/msft-10k_20180630.htm')
links.append('Companies/MSFT/2017_10-k.html')
links.append('Companies/MSFT/2016_10-k.html')
links.append('Companies/MSFT/2015_10-k.html')
links.append('Companies/MSFT/2014_10-k.html')
# links.append('Companies/MSFT/2013_10-k.html')


# for link in links:
#
#     report = af.create_pages(link)
#
#     toc = af.get_table_of_contents(report)
#     pn = af.get_page_num(report, toc)
#
#     statement = af.decimate_page(report.get("Page " + str(pn)))
#     # print("\n" + "NEXT STATEMENT" + "\n")
#     # print(af.dict_to_df(statement))
#     statements.append(statement)
#     if len(statements) == 2:
#         combo = af.combine_statements(statements[0], statements[1])
#         # print("\n" + "COMBO COMING" + "\n")
#         # print(af.dict_to_df(combo))
#     elif len(statements) > 2:
#         combo = af.combine_statements(combo, statements[-1])
#         # print("\n" + "COMBO COMING" + "\n")
#         # print(af.dict_to_df(combo))
#     else:
#         continue

all_finances = af.get_all_finances(links)
print()
print("INCOME")
print()
print(af.dict_to_df(all_finances[0]))
print()
print("BALANCE SHEET")
print()
print(af.dict_to_df(all_finances[1]))
print()
print("CASH FLOW")
print()
print(af.dict_to_df(all_finances[2]))
print()
print("EQUITY")
print()
print(af.dict_to_df(all_finances[3]))
print()
print("Execution time: " + str(time.time() - start))
