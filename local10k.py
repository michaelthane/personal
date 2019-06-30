import AllFunctions as af
import os
import bs4
import time
import pandas as pd
from dateutil.parser import parse
import re
import matplotlib.pyplot as plt
import numpy as np

start = time.time()

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)

links = []
statements = []
combo = {}

ticker = "MSFT"

if not os.path.exists("Companies/" + ticker + "/Clean"):
    af.clean(ticker)
    # links.extend()

for dir_tuple in os.walk("Companies/" + ticker + "/Clean", topdown=True):
    # print(dir_tuple)
    for file in dir_tuple[2]:
        if file.endswith(".txt"):
            links.append("Companies/" + ticker + "/Clean/" + file)
# Sort in descending order
links.sort(reverse=True)

# links.append('Companies/MSFT/2018_10-k.txt')
# links.append('Companies/MSFT/2017_10-k.txt')
# links.append('Companies/MSFT/2016_10-k.txt')
# links.append('Companies/MSFT/2015_10-k.txt')
# links.append('Companies/MSFT/2014_10-k.txt')
# links.append('Companies/MSFT/2013_10-k.txt')
# links.append('Companies/MSFT/2012_10-k.txt')
# links.append('Companies/MSFT/2011_10-k.txt')
# links.append('Companies/MSFT/2010_10-k.txt')
# links.append('Companies/MSFT/2009_10-k.txt')

# links.append('Companies/MS/Clean/2018_10-k.txt')
# links.append('Companies/MS/Clean/2017_10-k.txt')
# links.append('Companies/MS/Clean/2016_10-k.txt')
# links.append('Companies/MCD/Clean/2015_10-k.txt')
# links.append('Companies/MCD/Clean/2014_10-k.txt')
# links.append('Companies/MCD/Clean/2013_10-k.txt')
# links.append('Companies/MCD/Clean/2012_10-k.txt')
# links.append('Companies/MCD/Clean/2011_10-k.txt')
# links.append('Companies/MCD/Clean/2010_10-k.txt')
# links.append('Companies/MCD/Clean/2009_10-k.txt')

# pd.read_html()  # look into this...it could replace decimate_page()

for link in links:

    report = af.create_pages(link)

    toc = af.get_table_of_contents(report)
    pn = af.get_page_nums(report, toc)

    statement = af.decimate_page(report.get("Page " + str(pn[1])))
    print("\n" + "NEXT STATEMENT" + "\n")
    print(af.dict_to_df(statement))
    statements.append(statement)
    if len(statements) == 2:
        combo = af.display_combine_statements(statements[0], statements[1])
        print("\n" + "COMBO COMING" + "\n")
        print(af.dict_to_df(combo))
    elif len(statements) > 2:
        combo = af.display_combine_statements(combo, statements[-1])
        print("\n" + "COMBO COMING" + "\n")
        print(af.dict_to_df(combo))
    else:
        continue
'''
df = af.dict_to_df(combo)
print(df)
print()


"""Making final spreadsheet"""

col_headers = list(df)
df_len = len(col_headers) - 1

newDF = pd.DataFrame({col_headers[0]: col_headers[1:]})
print(newDF)
print()

idx = []
header_map = {}
header_pos = 1
# for rowname in df.iloc[:, 0]:
#     if re.search("revenue", rowname, flags=re.IGNORECASE) is not None and \
#        re.search(":", rowname) is None:
#         print(rowname)
#         # row_names.append(rowname)
#         idx.append(x)
#     elif re.search("margin", rowname, flags=re.IGNORECASE) is not None or \
#          re.search("net income", rowname, flags=re.IGNORECASE) is not None:
#         print(rowname)
#         idx.append(x)
#     elif re.search("share", rowname, flags=re.IGNORECASE) is not None and \
#          re.search(":", rowname) is not None:
#         # Check if next, next rowname is "diluted"
#         if re.search("diluted", next(next(iter(df.iloc[:, 0]))), flags=re.IGNORECASE) is not None:
#             print(rowname)
#             idx.append(x+2)
#     x += 1
for i in range(len(df.iloc[:, 0])):
    if re.search("revenue", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None and \
       re.search(":", df.iloc[:, 0][i]) is None and \
       re.search("total", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None:
        print(df.iloc[:, 0][i])
        # row_names.append(rowname)
        idx.append(i)
    elif re.search("margin", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None or \
         re.search("net income", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None or \
         re.search("dividend", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None:
        print(df.iloc[:, 0][i])
        idx.append(i)
    elif re.search("share", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None and \
         re.search(":", df.iloc[:, 0][i]) is not None and \
         re.search("diluted", df.iloc[:, 0][i + 2], flags=re.IGNORECASE) is not None:
        # Check if next, next rowname is "diluted"
        print(df.iloc[:, 0][i + 2])
        idx.append(i + 2)
    elif re.search("share", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None and \
         re.search(":", df.iloc[:, 0][i]) is None and \
         re.search("diluted", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None:
        # Check if next, next rowname is "diluted"
        print(df.iloc[:, 0][i])
        idx.append(i)

print()

epsFound = False

for i in idx:
    if re.search("diluted", df.iloc[i].values[0], flags=re.IGNORECASE):
        if not epsFound:
            new_col = {"EPS " + df.iloc[i].values[0]:
                       [float(elem.replace(",", "").replace("(", "").replace(")", "").replace("-", "0")) for elem in df.iloc[i].values[1:]]}
            epsFound = True
        else:
            new_col = {"Shares outstanding " + df.iloc[i].values[0]:
                       [float(elem.replace(",", "").replace("(", "").replace(")", "").replace("-", "0")) for elem in df.iloc[i].values[1:]]}
    else:
        new_col = {df.iloc[i].values[0]:
                   [float(elem.replace(",", "").replace("(", "").replace(")", "").replace("-", "0")) for elem in df.iloc[i].values[1:]]}
    # Have to make a col_name list because the column in the DF has not actually changed.
    col_name = list(new_col.keys())
    if not all(data == 0 for data in new_col.get(col_name[0])):
        while len(new_col.get(col_name[0])) < df_len:
            new_col.get(col_name[0]).append(0)
        header_map[col_name[0]] = header_pos
        header_pos += 1
        newDF[col_name[0]] = new_col.get(col_name[0])
print(newDF)
print("FINISHED WITH INCOME"+"\n")

"""Adding balance sheet"""

combo.clear()
statements.clear()
statement.clear()

for link in links:

    report = af.create_pages(link)

    toc = af.get_table_of_contents(report)
    pn = af.get_page_nums(report, toc)

    statement = af.decimate_page(report.get("Page " + str(pn[1])))
    # print("\n" + "NEXT STATEMENT" + "\n")
    # print(af.dict_to_df(statement))
    statements.append(statement)
    if len(statements) == 2:
        combo = af.display_combine_statements(statements[0], statements[1])
        # print("\n" + "COMBO COMING" + "\n")
        # print(af.dict_to_df(combo))
    elif len(statements) > 2:
        combo = af.display_combine_statements(combo, statements[-1])
        # print("\n" + "COMBO COMING" + "\n")
        # print(af.dict_to_df(combo))
    else:
        continue

df = af.dict_to_df(combo)

print(df)
print()

idx.clear()
x = 0
for rowname in df.iloc[:, 0]:
    if re.search("current", rowname, flags=re.IGNORECASE) is not None and \
       re.search(":", rowname) is None and re.search("other", rowname) is None and \
       re.search("debt", rowname, flags=re.IGNORECASE) is None:
        print(rowname)
        # row_names.append(rowname)
        idx.append(x)
    elif re.search("margin", rowname, flags=re.IGNORECASE) is not None or \
         re.search("net income", rowname, flags=re.IGNORECASE) is not None:
        print(rowname)
        idx.append(x)
    elif re.search("long-term debt", rowname, flags=re.IGNORECASE) is not None and \
         re.search("current", rowname, flags=re.IGNORECASE) is None:
        print(rowname)
        idx.append(x)
    elif re.search("equity", rowname, flags=re.IGNORECASE) is not None and \
         re.search("and", rowname, flags=re.IGNORECASE) is None and \
         re.search(":", rowname, flags=re.IGNORECASE) is None:
        print(rowname)
        idx.append(x)
    x += 1

print()

for i in idx:
    new_col = {df.iloc[i].values[0]:
               [float(elem.replace(",", "").replace("(", "").replace(")", "").replace("-", "0")) for elem in df.iloc[i].values[1:]]}
    # print(new_col)
    # print()
    if not all(data == 0 for data in new_col.get(df.iloc[i][0])):
        while len(new_col.get(df.iloc[i][0])) < df_len:
            new_col.get(df.iloc[i][0]).append(0)
        header_map[df.iloc[i][0]] = header_pos
        header_pos += 1
        newDF[df.iloc[i][0]] = new_col.get(df.iloc[i][0])
print(newDF)
print("DONE WITH BALANCE SHEET" + "\n")

"""Adding cash flow"""

combo.clear()
statements.clear()
statement.clear()

for link in links:

    report = af.create_pages(link)

    toc = af.get_table_of_contents(report)
    pn = af.get_page_nums(report, toc)

    statement = af.decimate_page(report.get("Page " + str(pn[2])))
    # print("\n" + "NEXT STATEMENT" + "\n")
    # print(af.dict_to_df(statement))
    statements.append(statement)
    if len(statements) == 2:
        combo = af.display_combine_statements(statements[0], statements[1])
        # print("\n" + "COMBO COMING" + "\n")
        # print(af.dict_to_df(combo))
    elif len(statements) > 2:
        combo = af.display_combine_statements(combo, statements[-1])
        # print("\n" + "COMBO COMING" + "\n")
        # print(af.dict_to_df(combo))
    else:
        continue

df = af.dict_to_df(combo)

print(df)
print()

idx.clear()
x = 0
for rowname in df.iloc[:, 0]:
    # if re.search("current", rowname, flags=re.IGNORECASE) is not None and \
    #    re.search(":", rowname) is None and re.search("debt", rowname, flags=re.IGNORECASE) is None:
    #     print(rowname)
    #     # row_names.append(rowname)
    #     idx.append(x)
    if re.search("dividend", rowname, flags=re.IGNORECASE) is not None:
        print(rowname)
        idx.append(x)
    # elif re.search("long-term debt", rowname, flags=re.IGNORECASE) is not None and \
    #      re.search("current", rowname, flags=re.IGNORECASE) is None:
    #     print(rowname)
    #     idx.append(x)
    # elif re.search("equity", rowname, flags=re.IGNORECASE) is not None and \
    #      re.search("and", rowname, flags=re.IGNORECASE) is None and \
    #      re.search(":", rowname, flags=re.IGNORECASE) is None:
    #     print(rowname)
    #     idx.append(x)
    x += 1

print()

for i in idx:
    new_col = {df.iloc[i].values[0]:
               [float(elem.replace(",", "").replace("(", "").replace(")", "").replace("-", "0")) for elem in df.iloc[i].values[1:]]}
    # print(new_col)
    # print()
    if not all(data == 0 for data in new_col.get(df.iloc[i][0])):
        while len(new_col.get(df.iloc[i][0])) < df_len:
            new_col.get(df.iloc[i][0]).append(0)
        header_map[df.iloc[i][0]] = header_pos
        header_pos += 1
        newDF[df.iloc[i][0]] = new_col.get(df.iloc[i][0])
print(newDF)
print("DONE WITH CASH FLOW" + "\n")

"""Adding equity statement"""

combo.clear()
statements.clear()
statement.clear()

for link in links:

    report = af.create_pages(link)

    toc = af.get_table_of_contents(report)
    pn = af.get_page_nums(report, toc)

    statement = af.decimate_page(report.get("Page " + str(pn[3])))
    # print("\n" + "NEXT STATEMENT" + "\n")
    # print(af.dict_to_df(statement))
    statements.append(statement)
    if len(statements) == 2:
        combo = af.display_combine_statements(statements[0], statements[1])
        # print("\n" + "COMBO COMING" + "\n")
        # print(af.dict_to_df(combo))
    elif len(statements) > 2:
        combo = af.display_combine_statements(combo, statements[-1])
        # print("\n" + "COMBO COMING" + "\n")
        # print(af.dict_to_df(combo))
    else:
        continue

df = af.dict_to_df(combo)


"""Making final spreadsheet"""

print(df)
print()

idx.clear()
x = 0
for rowname in df.iloc[:, 0]:
    # if re.search("current", rowname, flags=re.IGNORECASE) is not None and \
    #    re.search(":", rowname) is None and re.search("debt", rowname, flags=re.IGNORECASE) is None:
    #     print(rowname)
    #     # row_names.append(rowname)
    #     idx.append(x)
    if re.search("dividend", rowname, flags=re.IGNORECASE) is not None:
        print(rowname)
        idx.append(x)
    # elif re.search("long-term debt", rowname, flags=re.IGNORECASE) is not None and \
    #      re.search("current", rowname, flags=re.IGNORECASE) is None:
    #     print(rowname)
    #     idx.append(x)
    # elif re.search("equity", rowname, flags=re.IGNORECASE) is not None and \
    #      re.search("and", rowname, flags=re.IGNORECASE) is None and \
    #      re.search(":", rowname, flags=re.IGNORECASE) is None:
    #     print(rowname)
    #     idx.append(x)
    x += 1

print()

for i in idx:
    new_col = {df.iloc[i].values[0]:
               [float(elem.replace(",", "").replace("(", "").replace(")", "").replace("-", "0")) for elem in df.iloc[i].values[1:]]}
    # print(new_col)
    # print()
    if not all(data == 0 for data in new_col.get(df.iloc[i][0])):
        while len(new_col.get(df.iloc[i][0])) < df_len:
            new_col.get(df.iloc[i][0]).append(0)
        header_map[df.iloc[i][0]] = header_pos
        header_pos += 1
        newDF[df.iloc[i][0]] = new_col.get(df.iloc[i][0])
print(newDF)
print("DONE WITH EQUITY" + "\n")
print(af.dict_to_df(header_map, transpose=True))
print()

# Drop columns with all zeros, might never add zero columns
# print(newDF)
# del_keys = []
# for key in list(header_map.keys()):
#     if all(data == 0 for data in newDF.iloc[:, header_map.get(key)].values):
#         del_keys.append(key)
# newDF.drop(labels=del_keys, axis=1, inplace=True)
# print(newDF)

print(af.dict_to_df(header_map, transpose=True))
keys = list(header_map.keys())
print(keys)


"""Adding T3M EPS"""
# Make T3M EPS
for key in keys:
    if re.search("eps", key, flags=re.IGNORECASE) is not None:
        eps_key = key
        eps = newDF.iloc[:, header_map.get(key)].values
t3m = []
for i in range(len(eps)-2):
    # avg = (eps[i] + eps[i+1] + eps[i+2]) / 3
    t3m.append(round((eps[i] + eps[i+1] + eps[i+2]) / 3, 2))
while len(t3m) < df_len:
    t3m.append(0)

# Adjust header map
insert_col_num = header_map.get(eps_key)
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "T3M EPS"
header_map[new_col_name] = insert_col_num + 1

# Insert T3M into DF
newDF.insert(header_map.get(new_col_name), new_col_name, t3m)

# Make desired entry price based on T3M
entryt3m = []
multiplier = 25
for i in range(len(t3m)):
    entryt3m.append(round(t3m[i] * multiplier, 2))
while len(entryt3m) < df_len:
    entryt3m.append(0)

# Adjust header map
insert_col_num = header_map.get(new_col_name)
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Entry Price, T3M"
header_map[new_col_name] = insert_col_num + 1

# Insert Entry Price, T3M into DF
newDF.insert(header_map.get(new_col_name), new_col_name, entryt3m)
print(newDF)
print()


"""Adding Assets / Liabilities ratio"""
# Make Assets to Liabilities ratio
for key in keys:
    if re.search("assets", key, flags=re.IGNORECASE) is not None:
        assets_key = key
        assets = newDF.iloc[:, header_map.get(key)].values
    if re.search("liabilities", key, flags=re.IGNORECASE) is not None:
        liabilities_key = key
        liabilities = newDF.iloc[:, header_map.get(key)].values

print(assets)
print(liabilities)
al_ratio = []
for i in range(min(len(assets), len(liabilities))):
    if liabilities[i] != 0:
        al_ratio.append(round(assets[i] / liabilities[i], 2))
    else:
        al_ratio.append(0)
while len(al_ratio) < df_len:
    al_ratio.append(0)

# Adjust header map
insert_col_num = max(header_map.get(assets_key), header_map.get(liabilities_key))
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Assets / Liabilities"
header_map[new_col_name] = insert_col_num + 1
print(af.dict_to_df(header_map, transpose=True))

# Insert Asset / Liabilities ratio int DF
newDF.insert(header_map.get(new_col_name), new_col_name, al_ratio)
print(newDF)
print()


"""Adding Debt / Capital (Equity) ratio"""
# Make Debt to Capital ratio
for key in keys:
    if re.search("debt", key, flags=re.IGNORECASE) is not None:
        debt_key = key
        debt = newDF.iloc[:, header_map.get(key)].values
    if re.search("equity", key, flags=re.IGNORECASE) is not None:
        equity_key = key


# capital = [float(decStr.replace(",", "").replace("-", "0"))
#            for decStr in newDF.iloc[:, header_map.get("Total stockholders’ equity")].values]
capital = []
for i in range(min(len(assets), len(liabilities))):
    if liabilities[i] != 0:
        capital.append(round(assets[i] - liabilities[i], 2))
    else:
        capital.append(0)
while len(capital) < df_len:
    capital.append(0)
print(debt)
print(capital)
dc_ratio = []
for i in range(min(len(debt), len(capital))):
    if capital[i] != 0:
        dc_ratio.append(round(debt[i] / capital[i], 2))
    else:
        dc_ratio.append(0)
while len(dc_ratio) < df_len:
    dc_ratio.append(0)

# Adjust header map
insert_col_num = max(header_map.get(debt_key), header_map.get(equity_key))
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Capital"
header_map[new_col_name] = insert_col_num + 1

# Insert capital values into DF
newDF.insert(header_map.get(new_col_name), new_col_name, capital)

# Adjust header map
insert_col_num = header_map.get(new_col_name)
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Debt / Capital"
header_map[new_col_name] = insert_col_num + 1

# Insert Debt / Capital ratio into DF
newDF.insert(header_map.get(new_col_name), new_col_name, dc_ratio)
print(newDF)
print()


"""Adding Net Asset Value"""
# Make NAV
for key in keys:
    if re.search("outstanding", key, flags=re.IGNORECASE) is not None:
        shares_outstanding_key = key
        shares = newDF.iloc[:, header_map.get(key)].values
nav = []
for i in range(min(len(capital), len(shares))):
    if shares[i] != 0:
        nav.append(round(capital[i] / shares[i], 2))
    else:
        nav.append(0)
while len(nav) < df_len:
    nav.append(0)

# Adjust header map
insert_col_num = header_map.get(shares_outstanding_key)
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "NAV"
header_map[new_col_name] = insert_col_num + 1
print(af.dict_to_df(header_map, transpose=True))

# Insert NAV into DF
newDF.insert(header_map.get(new_col_name), new_col_name, nav)
print(newDF)
print()


"""Adding Desired NAV Entry Price"""
# Make Entry Price, NAV
entryNAV = []
multiplier = 1.5
for i in range(len(nav)):
    entryNAV.append(round(nav[i] * multiplier, 2))
while len(entryNAV) < df_len:
    entryNAV.append(0)

# Adjust header map
insert_col_num = header_map.get("NAV")
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Entry Price, NAV"
header_map[new_col_name] = insert_col_num + 1
print(af.dict_to_df(header_map, transpose=True))

# Insert Entry Price, NAV into DF
newDF.insert(header_map.get(new_col_name), new_col_name, entryNAV)
print(newDF)
print()


"""Adding ROE (Net Income / Equity)"""
# Make ROE (%)
for key in keys:
    if re.search("income", key, flags=re.IGNORECASE) is not None:
        income_key = key
        income = newDF.iloc[:, header_map.get(key)].values
# income = newDF.iloc[:, header_map.get("Net income")].values
equity = newDF.iloc[:, header_map.get(equity_key)].values
print(income)
print(equity)
roe = []
for i in range(min(len(income), len(equity))):
    if equity[i] != 0:
        # Append as percentage
        roe.append(round((income[i] / equity[i]) * 100, 2))
    else:
        roe.append(0)
while len(roe) < df_len:
    roe.append(0)

# Adjust header map
insert_col_num = header_map.get(income_key)
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "ROE (%)"
header_map[new_col_name] = insert_col_num + 1
print(af.dict_to_df(header_map, transpose=True))

# Insert ROE (%) into DF
newDF.insert(header_map.get(new_col_name), new_col_name, roe)
print(newDF)
print()


"""Adding Net PM (Net Income / Total Revenue)"""
# Make Net PM (%)
for key in keys:
    if re.search("revenue", key, flags=re.IGNORECASE) is not None:
        revenue_key = key
        revenue = newDF.iloc[:, header_map.get(key)].values
print(revenue)
pm = []
for i in range(min(len(income), len(revenue))):
    if revenue[i] != 0:
        # Append as percentage
        pm.append(round((income[i] / revenue[i]) * 100, 2))
    else:
        pm.append(0)
while len(pm) < df_len:
    pm.append(0)

# Adjust header map
insert_col_num = header_map.get(revenue_key)
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Net PM (%)"
header_map[new_col_name] = insert_col_num + 1
print(af.dict_to_df(header_map, transpose=True))

# Insert Net PM (%) into DF
newDF.insert(header_map.get(new_col_name), new_col_name, pm)
print(newDF)
print()


"""Adding Div per share"""
# Make DPS
for key in keys:
    if re.search("dividend", key, flags=re.IGNORECASE) is not None:
        dividend_key = key
        div = newDF.iloc[:, header_map.get(key)].values
print(div)
dps = []
for i in range(min(len(div), len(shares))):
    if shares[i] != 0:
        dps.append(round(div[i] / shares[i], 2))
    else:
        dps.append(0)
while len(dps) < df_len:
    dps.append(0)

    # Adjust header map
insert_col_num = header_map.get(dividend_key)
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "DPS"
header_map[new_col_name] = insert_col_num + 1
print(af.dict_to_df(header_map, transpose=True))

# Insert DPS into DF
newDF.insert(header_map.get(new_col_name), new_col_name, dps)
print(newDF)
print()



# plt.ylim([35, 70])
plt.scatter([int(year) for year in newDF.iloc[:, 0].values],
            [float(elem) for elem in newDF.iloc[:, header_map.get("Entry Price, T3M")].values])
plt.plot([int(year) for year in newDF.iloc[:, 0].values],
         [float(elem) for elem in newDF.iloc[:, header_map.get("Entry Price, T3M")].values])
# plt.plot([int(year) for year in newDF.iloc[:, 0].values],
#          float(newDF.iloc[:, header_map.get("Entry Price, T3M")].values[2]))
# plt.subplot([int(year) for year in newDF.iloc[:, 0].values],
#             newDF.iloc[:, header_map.get("ROE (%)")].values)
plt.gcf().autofmt_xdate()
plt.show()

# pd.DataFrame.to_csv()
# newDF.to_csv("yahyeet.csv", index=False)


"""DO NOT TOUCH BELOW HERE"""

# all_finances = af.get_all_finances(links)
# print()
# print("INCOME")
# print()
# print(af.dict_to_df(all_finances[0]))
# print()
# print("BALANCE SHEET")
# print()
# print(af.dict_to_df(all_finances[1]))
# print()
# print("CASH FLOW")
# print()
# print(af.dict_to_df(all_finances[2]))
# print()
# print("EQUITY")
# print()
# print(af.dict_to_df(all_finances[3]))
# print()
# print("Execution time: " + str(time.time() - start))
'''

