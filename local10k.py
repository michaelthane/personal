import AllFunctions as af
import os
import bs4
import time
import pandas as pd
from collections import OrderedDict
from dateutil.parser import parse


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




report1 = af.create_pages('Companies/MSFT/msft-10k_20180630.htm')
report2 = af.create_pages('Companies/MSFT/msft-10k_20170630.htm')

# report = af.create_pages('Companies/MSFT/d10k.htm')
#print(report)
#print(af.dict_to_df(report, transpose=True))
#toc = af.get_table_of_contents(report1)
#print(af.dict_to_df(toc, transpose=True))
# Get page numbers of Item 8 and such from the table of contents.
# print(pd.DataFrame(data=table_of_contents, index=[0]).transpose())
# print()
pd.set_option('display.max_columns', None)
statement1 = af.decimate_page(report1.get("Page 52"), {}, [])
print(af.dict_to_df(statement1))
print()
print("NEXT STATEMENT")
print()
statement2 = af.decimate_page(report2.get("Page 50"), {}, [])
print(af.dict_to_df(statement2))
print()
print("COMBO COMING")
print()
combo = af.combine_statements(statement1, statement2)
print(af.dict_to_df(combo))
#print(af.decimate_page(report.get("Page 51")))
#print(af.decimate_page(report.get("Page 52"), {}, []))
#print(af.decimate_page(report.get("Page 53")))
#print(af.decimate_page(report.get("Page 54")))

# soup2 = bs4.BeautifulSoup(report.get("Page 53"), 'html.parser')

# for elem in soup2.stripped_strings:
#     print(elem)

