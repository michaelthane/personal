import AllFunctions as af
import os
import bs4
import time
import pandas as pd
from dateutil.parser import parse
import re

start = time.time()

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)

links = []
statements = []
combo = {}

ticker = "WMT"

if not os.path.exists("Companies/" + ticker + "/Clean"):
    af.clean(ticker)

links.append('Companies/MSFT/2018_10-k.txt')
links.append('Companies/MSFT/2017_10-k.txt')
links.append('Companies/MSFT/2016_10-k.txt')
links.append('Companies/MSFT/2015_10-k.txt')
links.append('Companies/MSFT/2014_10-k.txt')
links.append('Companies/MSFT/2013_10-k.txt')
links.append('Companies/MSFT/2012_10-k.txt')
links.append('Companies/MSFT/2011_10-k.txt')
links.append('Companies/MSFT/2010_10-k.txt')
links.append('Companies/MSFT/2009_10-k.txt')

# links.append('Companies/WMT/Clean/2018_10-k.txt')
# links.append('Companies/WMT/Clean/2016_10-k.txt')
# links.append('Companies/WMT/2017_10-k.html')
# links.append('Companies/WMT/2016_10-k_aux.html')
# links.append('Companies/MSFT/2015_10-k.html')
# links.append('Companies/MSFT/2014_10-k.html')
# links.append('Companies/MSFT/2013_10-k.html')

# links.append('Companies/MCD/Clean/2018_10-k.txt')
# links.append('Companies/MCD/Clean/2017_10-k.txt')

# pd.read_html()  # look into this...it could replace decimate_page()

for link in links:

    report = af.create_pages(link)

    toc = af.get_table_of_contents(report)
    pn = af.get_page_nums(report, toc)

    statement = af.decimate_page(report.get("Page " + str(pn[0])))
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
       re.search(":", df.iloc[:, 0][i]) is None:
        print(df.iloc[:, 0][i])
        # row_names.append(rowname)
        idx.append(i)
    elif re.search("margin", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None or \
         re.search("net income", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None or \
         re.search("dividend", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None:
        print(df.iloc[:, 0][i])
        idx.append(i)
    elif re.search("share", df.iloc[:, 0][i], flags=re.IGNORECASE) is not None and \
         re.search(":", df.iloc[:, 0][i]) is not None:
        # Check if next, next rowname is "diluted"
        if re.search("diluted", df.iloc[:, 0][i+2], flags=re.IGNORECASE) is not None:
            print(df.iloc[:, 0][i+2])
            idx.append(i+2)

print()

epsFound = False

for i in idx:
    if re.search("diluted", df.iloc[i].values[0], flags=re.IGNORECASE):
        if not epsFound:
            new_col = {"EPS " + df.iloc[i].values[0]: list(df.iloc[i].values[1:])}
            epsFound = True
        else:
            new_col = {"Shares outstanding " + df.iloc[i].values[0]: list(df.iloc[i].values[1:])}
    else:
        new_col = {df.iloc[i].values[0]: list(df.iloc[i].values[1:])}
    # print(new_col)
    # print()
    list1 = list(new_col.keys())
    while len(new_col.get(list1[0])) < df_len:
        new_col.get(list1[0]).append("-")
    header_map[list1[0]] = header_pos
    header_pos += 1
    newDF[list1[0]] = new_col.get(list1[0])
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
       re.search(":", rowname) is None and re.search("debt", rowname, flags=re.IGNORECASE) is None:
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
    new_col = {df.iloc[i].values[0]: list(df.iloc[i].values[1:])}
    # print(new_col)
    # print()
    while len(new_col.get(df.iloc[i][0])) < df_len:
        new_col.get(df.iloc[i][0]).append("-")
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
    new_col = {df.iloc[i].values[0]: list(df.iloc[i].values[1:])}
    # print(new_col)
    # print()
    while len(new_col.get(df.iloc[i][0])) < df_len:
        new_col.get(df.iloc[i][0]).append("-")
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
    new_col = {df.iloc[i].values[0]: list(df.iloc[i].values[1:])}
    # print(new_col)
    # print()
    while len(new_col.get(df.iloc[i][0])) < df_len:
        new_col.get(df.iloc[i][0]).append("-")
    header_map[df.iloc[i][0]] = header_pos
    header_pos += 1
    newDF[df.iloc[i][0]] = new_col.get(df.iloc[i][0])
print(newDF)
print("DONE WITH EQUITY" + "\n")
print(af.dict_to_df(header_map, transpose=True))
print()


"""Adding T3M EPS"""
eps = [float(decStr) for decStr in newDF.iloc[:, header_map.get("EPS Diluted")].values]
t3m = []
for i in range(len(eps)-2):
    avg = (eps[i] + eps[i+1] + eps[i+2]) / 3
    t3m.append(str(round(avg, 2)))
while len(t3m) < df_len:
    t3m.append("-")
insert_col_num = header_map.get("EPS Diluted")
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "T3M EPS"
header_map[new_col_name] = insert_col_num + 1
newDF.insert(header_map.get(new_col_name), new_col_name, t3m)
entryt3m = []
multiplier = 25
for i in range(len(t3m)):
    entryt3m.append(str(round(float(t3m[i].replace("-", "0")) * multiplier, 2)))
while len(entryt3m) < df_len:
    entryt3m.append("-")
insert_col_num = header_map.get(new_col_name)
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Entry Price, T3M"
header_map[new_col_name] = insert_col_num + 1
newDF.insert(header_map.get(new_col_name), new_col_name, entryt3m)
print(newDF)
print()


"""Adding Assets / Liabilities ratio"""
assets = [float(decStr.replace(",", "").replace("-", "0"))
          for decStr in newDF.iloc[:, header_map.get("Total current assets")].values]
liabilities = [float(decStr.replace(",", "").replace("-", "0"))
               for decStr in newDF.iloc[:, header_map.get("Total current liabilities")].values]
print(assets)
print(liabilities)
al_ratio = []
for i in range(min(len(assets), len(liabilities))):
    if liabilities[i] != 0:
        al_ratio.append(str(round(assets[i] / liabilities[i], 2)))
    else:
        al_ratio.append("-")
while len(al_ratio) < df_len:
    al_ratio.append("-")
insert_col_num = max(header_map.get("Total current assets"), header_map.get("Total current liabilities"))
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Assets / Liabilities"
header_map[new_col_name] = insert_col_num + 1

print(af.dict_to_df(header_map, transpose=True))
newDF.insert(header_map.get(new_col_name), new_col_name, al_ratio)
print(newDF)
print()


"""Adding Debt / Capital (Equity) ratio"""
debt = [float(decStr.replace(",", "").replace("-", "0"))
        for decStr in newDF.iloc[:, header_map.get("Long-term debt")].values]
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
        dc_ratio.append(str(round(debt[i] / capital[i], 2)))
    else:
        dc_ratio.append("-")
while len(dc_ratio) < df_len:
    dc_ratio.append("-")
insert_col_num = max(header_map.get("Long-term debt"), header_map.get("Total stockholders’ equity"))
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Capital"
header_map[new_col_name] = insert_col_num + 1

newDF.insert(header_map.get(new_col_name), new_col_name, capital)

insert_col_num = header_map.get(new_col_name)
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Debt / Capital"
header_map[new_col_name] = insert_col_num + 1

newDF.insert(header_map.get(new_col_name), new_col_name, dc_ratio)
print(newDF)
print()


"""Adding Net Asset Value"""
shares = [float(decStr.replace(",", "").replace("-", "0"))
          for decStr in newDF.iloc[:, header_map.get("Shares outstanding Diluted")].values]
nav = []
for i in range(min(len(capital), len(shares))):
    if shares[i] != 0:
        nav.append(str(round(capital[i] / shares[i], 2)))
    else:
        nav.append("-")
while len(nav) < df_len:
    nav.append("-")
insert_col_num = header_map.get("Shares outstanding Diluted")
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "NAV"
header_map[new_col_name] = insert_col_num + 1

print(af.dict_to_df(header_map, transpose=True))
newDF.insert(header_map.get(new_col_name), new_col_name, nav)
print(newDF)
print()


"""Adding Desired NAV Entry Price"""
entryNAV = []
multiplier = 1.5
for i in range(len(nav)):
    entryNAV.append(str(round(float(nav[i].replace(",", "").replace("-", "0")) * multiplier, 2)))
while len(entryNAV) < df_len:
    entryNAV.append("-")
insert_col_num = header_map.get("NAV")
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "Entry Price, NAV"
header_map[new_col_name] = insert_col_num + 1

print(af.dict_to_df(header_map, transpose=True))
newDF.insert(header_map.get(new_col_name), new_col_name, entryNAV)
print(newDF)
print()


"""Adding ROE (Net Income / Equity)"""
income = [float(decStr.replace(",", "").replace("-", "0"))
          for decStr in newDF.iloc[:, header_map.get("Net income")].values]
equity = [float(decStr.replace(",", "").replace("-", "0"))
          for decStr in newDF.iloc[:, header_map.get("Total stockholders’ equity")].values]
print(income)
print(equity)
roe = []
for i in range(min(len(income), len(equity))):
    if equity[i] != 0:
        roe.append(str(round((income[i] / equity[i]) * 100, 2)))
    else:
        roe.append("-")
while len(roe) < df_len:
    roe.append("-")
insert_col_num = header_map.get("Net income")
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "ROE"
header_map[new_col_name] = insert_col_num + 1

print(af.dict_to_df(header_map, transpose=True))
newDF.insert(header_map.get(new_col_name), new_col_name, roe)
print(newDF)
print()


"""Adding Net PM (Net Income / Total Revenue)"""
revenue = [float(decStr.replace(",", "").replace("-", "0"))
           for decStr in newDF.iloc[:, header_map.get("Total revenue")].values]
print(revenue)
pm = []
for i in range(min(len(income), len(revenue))):
    if revenue[i] != 0:
        pm.append(str(round((income[i] / revenue[i]) * 100, 2)))
    else:
        pm.append("-")
while len(pm) < df_len:
    pm.append("-")
insert_col_num = header_map.get("Total revenue")
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "PM"
header_map[new_col_name] = insert_col_num + 1

print(af.dict_to_df(header_map, transpose=True))
newDF.insert(header_map.get(new_col_name), new_col_name, pm)
print(newDF)
print()


"""Adding Div per share"""
div = [float(decStr.replace(",", "").replace("(", "").replace(")", ""))
           for decStr in newDF.iloc[:, header_map.get("Common stock cash dividends paid")].values]
print(div)
dps = []
for i in range(min(len(div), len(shares))):
    if shares[i] != 0:
        dps.append(str(round(div[i] / shares[i], 2)))
    else:
        dps.append("-")
while len(dps) < df_len:
    dps.append("-")
insert_col_num = header_map.get("Common stock cash dividends paid")
for key in list(header_map.keys()):
    if header_map.get(key) > insert_col_num:
        header_map[key] = header_map.get(key) + 1
new_col_name = "DPS"
header_map[new_col_name] = insert_col_num + 1

print(af.dict_to_df(header_map, transpose=True))
newDF.insert(header_map.get(new_col_name), new_col_name, dps)
print(newDF)
print()

# pd.DataFrame.to_csv()
newDF.to_csv("yahyeet.csv", index=False)


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
