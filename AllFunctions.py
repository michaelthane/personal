"""
Creator: Michael Thane
Last Revised: 3/4/2019
Description: This library contains any and all functions used throughout this application.
             This will improve readability and organization.
"""

import bs4
from dateutil.parser import parse
import pandas as pd
import re
import time


# Determine if string is a number
def is_number(string):
    """
    Return whether the string can be interpreted as a number.
    
    :param string: str, string to check for number
    :return: bool
    """
    # exclusions = [',', '$', '(', ')']
    try:
        # for x in exclusions:
        float(string.replace(',', '').replace('(', ''))
        return True
    except ValueError:
        return False


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def get_values(analyzing_value, tags):
    """
    Return a list ...
    Get list of values indicated by analyzing_value.
    When using is_number(), remove unicode in string.

    :param analyzing_value: 
    :param tags: 
    :return: list
    """
    return_list = []
    return_set = set()
    for elem in tags:
        correct_row = 0
        sub_tags = elem.select('td')
        for data in sub_tags:
            # Clean string to raw value
            # Check if the table data text equals the requested value
            if data.text.strip('\n') == analyzing_value and data.text.strip('\n') not in return_set:
                correct_row = 1
                return_list.append(data.text.strip('\n'))
                return_set.add(data.text.strip('\n'))
            if is_number(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', '')
                         .replace(u'\xa0', '')) \
                    and is_number(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', '')
                                  .replace(u'\xa0', '')) not in return_set\
                    and correct_row == 1:
                return_list.append(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', '')
                                   .replace(u'\xa0', ''))
                return_set.add(data.text.strip('\n').replace(',', '').replace('(', '').replace(')', '')
                                   .replace(u'\xa0', ''))
    return return_list


def parse10k(path):
    """
    Return a dataframe of values from input file.
    
    :param path:  str, file path
    :return: pandas.DataFrame()
    """
    soup = bs4.BeautifulSoup(open(path), 'html.parser')

    attribute_list = soup.select('tr')

    # The strings are hardcoded for this specific company.
    # Future work must make it possible for ANY company.
    liabilities      = get_values("Total liabilities", attribute_list)
    assets           = get_values("Total assets", attribute_list)
    debt             = get_values("Long-term debt", attribute_list)
    equity           = get_values("Total stockholders’ equity", attribute_list)
    dilutedEPS       = get_values("Diluted earnings per share", attribute_list)
    dividends        = get_values("Common stock cash dividends paid", attribute_list)
    netIncome        = get_values("Net income", attribute_list)
    totalRevenue     = get_values("Total revenue", attribute_list)
    retainedEarnings = get_values("Retained earnings", attribute_list)

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
    # pprint(get_values("Year Ended June 30,", attribute_list))

    list_of_lists = [liabilities,
                     assets,
                     debt,
                     equity,
                     dilutedEPS,
                     dividends,
                     netIncome,
                     totalRevenue,
                     retainedEarnings]

    # Find finance that has the most elements.
    longest_len = 0
    for thisList in list_of_lists:
        if len(thisList[1:]) > longest_len:
            longest_len = len(thisList[1:])

    # Add zeros for finances that have less than the max.
    for thisList in list_of_lists:
        if len(thisList[1:]) < longest_len:
            for i in range(longest_len - len(thisList[1:])):
                thisList.append(0)

    value_dict = {}
    for thisList in list_of_lists:
        value_dict[thisList[0]] = thisList[1:]

    # print(value_dict)

    df = pd.DataFrame(data=value_dict)

    pd.set_option('display.max_columns', 20)

    return df


def create_pages(path):
    """
    Return report after splitting by page break (<hr> -> horizontal row)
    ACTION: How to identify a page break?

    :param path: str, file path
    :return: dict, {"Page #" : tags}
    """
    file = open(path)
    report = dict()
    tags = ""
    page_num = 0
    for line in file:
        tags += line
        # If line starts with "<hr " (horizontal row), store string and go to next page.
        if line[:4] == "<hr " or line[:16] == '</p><hr size="3"':  # ACTION: This really shouldn't be hard-coded...
            report["Page " + str(page_num)] = tags
            tags = ""
            page_num += 1
    return report


def get_table_of_contents(pages):

    toc_page_number = ""
    for key in pages:
        # print(key)
        if re.search("index", pages.get(key), flags=re.IGNORECASE):
            toc_page_number = key
            break

    table_of_contents = {}
    chapter = ""
    soup = bs4.BeautifulSoup(pages.get(toc_page_number), 'html.parser')

    # If any of the stripped strings equals index or table of contents or the like, store pages and numbers and break
    for elem in soup.stripped_strings:
        elem = elem.replace(u"\xa0", u" ")
        if is_number(elem):
            table_of_contents[chapter] = int(elem)
            chapter = ""
        else:
            chapter += elem + " "
    table_of_contents.popitem()
    return table_of_contents


def get_page_num(report, toc, pattern="Item 8"):
    correct_page = False
    max_check = 10
    page_num = 0
    for key in toc:
        if re.search(pattern, key, flags=re.IGNORECASE):
            page_num = toc.get(key)
            break
    page_num -= 2
    for i in range(max_check):
        current = 0
        page_num += 1
        soup = bs4.BeautifulSoup(report.get("Page " + str(page_num)), 'html.parser')
        for elem in soup.stripped_strings:
            # See if this is the right page.
            if current < max_check:
                if re.search(pattern, elem, flags=re.IGNORECASE) is not None or \
                   re.search("financial", elem, flags=re.IGNORECASE) is not None or \
                   re.search("statements", elem, flags=re.IGNORECASE) is not None:
                    correct_page = True
                    break
            else:
                break
            current += 1
        if correct_page:
            break

    return "Page " + str(page_num)


def dict_to_df(dictionary, transpose=False):
    """
    Return the given dictionary as a DataFrame.

    :param dictionary: dict
    :param transpose: bool
    :return: pd.DataFrame()
    """
    return pd.DataFrame(data=dictionary, index=[0]).T if transpose else pd.DataFrame(data=dictionary)


# Return a dataframe of the financial data at file path.
# Probably call this separately for table...
def decimate_page(file_path):

    if len(file_path) < 260:  # MAX_PATH length
        soup = bs4.BeautifulSoup(open(file_path), 'html.parser')
    else:
        soup = bs4.BeautifulSoup(file_path, 'html.parser')

    # Initialize
    col_lens = []
    flag = 0
    longer_col = 0
    num_cols = 0
    pos = 0
    skip = False
    table = {}
    col_names = []

    # list of strings to be excluded
    # DO NOT DELETE "ITEM 8."; It is a special string with &nbsp; hidden in it.
    exclusions = ["millions", "PART II", "item", "FINANCIAL", "statement"]
    #exclusions = ["millions", "PART II", "Item 8", "ITEM 8.", "item", "FINANCIAL", "ITEM 8. FINANCIAL STATE"]
    for elem in soup.stripped_strings:

        # Starting with the date, the first row will be the col names; otherwise, skip that elem.
        if pos == 0:
            for exclude in exclusions:
                # print(exclude)
                #print(re.search(exclude, elem, flags=re.IGNORECASE))
                if re.search(exclude, elem, flags=re.IGNORECASE) is not None:
                #    print("skip")
                    skip = True
                    break
                else:
                    skip = False
                    continue
            if skip or not is_date(elem, fuzzy=True):
                continue
            else:
                # First elem should be a date like 'June 30' or similar.
                table[elem] = []  # key = elem : value = list
                col_names.append(elem)
                num_cols += 1
                pos += 1
            # print(elem)

            # if not is_date(elem, fuzzy=True) or elem in exclusions:
            #     continue
            # else:
            #     # First elem should be a date like 'June 30' or similar.
            #     table[elem] = []  # key = elem : value = list
            #     col_names.append(elem)
            #     num_cols += 1
            #     pos += 1
        elif elem == "$" or elem == ")":
            # How to not hard-code these exclusions?
            continue
        elif is_number(elem) and pos < num_cols + 1:
            # elem should be years like '2018' or '2017' or similar.
            table[elem] = []
            col_names.append(elem)
            pos += 1
            num_cols += 1
        elif (elem[0] == "$" or elem[:3] == "and") and len(elem) > 1:
            """
            Balance sheet displays number of outstanding stocks.
            The first outstanding number is seen as a legit number and will be put in the first year column.
            When you see the next outstanding number, it will be preceded with "and", but everything is out of order.
            """

            # Check if year columns are different length.
            # If so, then and elem was inserted into dict out of order.
            for i in range(1, len(col_names) - 1):
                flag = len(table.get(col_names[i])) - len(table.get(col_names[i+1]))
                if flag != 0:
                    longer_col = i

            if elem[:3] == "and" and flag != 0:
                table.get(col_names[0])[-1] += " " + table.get(col_names[longer_col]).pop() + elem
                flag = 0
                pos -= 1
            else:
                # If description column has numeric values, include them in description.
                table.get(col_names[0])[-1] += " " + elem
        elif not is_number(elem) and pos >= num_cols:

            # If col_lens hasn't been created yet, create it.
            if len(col_lens) == 0:
                col_lens = [0] * len(col_names)

            # If it is not a number and not in exclusions list, it will ALWAYS go in the first column.
            table.get(col_names[0]).append(elem)

            # Update differences in array length.
            for i in range(len(col_names)):
                col_lens[i] = len(table.get(col_names[0])) - len(table.get(col_names[i]))

            if (pos % num_cols) != 0 and sum(col_lens) != 0:
                for i in range(1, len(col_names)):
                    for j in range(col_lens[i] - 1):
                        table.get(col_names[i]).append("-")
                        pos += 1
            pos += 1
        elif is_number(elem) and pos > num_cols:
            # Put financial value in appropriate position.
            if elem[0] == "(":
                elem += ")"
            table.get(col_names[pos % num_cols]).append(elem)
            pos += 1

    # Adjust because of last row, which contains "refer to notes" and page number and only fills first year column.
    for i in range(1, len(col_names)):
        if len(table.get(col_names[0])) > len(table.get(col_names[i])):
            for j in range((len(table.get(col_names[0])) - len(table.get(col_names[i])))):
                table.get(col_names[i]).append("-")

    return table


def combine_statements(dict1, dict2):
    """
    Combine two statements from different reports.
    Check if the lowercase of strings are EXACTLY the same or if strings one index apart are EXACTLY the same.
    If not, check if strings are MOSTLY the same (the LCS of the two strings equals at least HALF of the first string.
    if not, check if strings one index apart are MOSTLY the same.

    :param dict1: dict, main report
    :param dict2: dict, auxiliary report
    :return: dict, dict1 with unique pairs from dict2
    """

    dict1_keys = []
    dict2_keys = []
    for key in dict1:
        dict1_keys.append(key)
    for key in dict2:
        dict2_keys.append(key)
    dict1_first_col = dict1.get(dict1_keys[0])
    dict2_first_col = dict2.get(dict2_keys[0])
    pos1 = 0
    pos2 = 0
    buffer = 2  # Used on very specific use cases.
    for key in dict2:
        if not is_number(key):
            """Don't look at date key ... "June 30," or similar."""
            continue
        elif key in dict1:
            """Year is already included in dict1"""
            continue
        else:
            """Never before seen year. Edit dict2 array to match dict1 before putting pair in dict1.
            Compare elements in column 0 from dict1 with elems in column 0 from dict2."""
            # print("key: " + key)
            while pos1 < len(dict1_first_col) and pos2 < len(dict2_first_col) - 1:
                """Check if strings are exactly the same. dict1 is always right."""
                # print()
                # print("length of dict1: " + str(len(dict1_first_col)))
                # print("length of dict2 col 0: " + str(len(dict2_first_col)))
                # print("length of dict2: " + str(len(dict2.get(key))))
                # print("pos1: " + str(pos1) + " | " + "pos2: " + str(pos2))
                # print(dict1_first_col[pos1] + "|vs|" + dict2_first_col[pos2])
                # print("difference: " +
                #       str(len(dict1_first_col[pos1]) - lcs(dict1_first_col[pos1], dict2_first_col[pos2])))
                # print("half of dict1: " + str(len(dict1_first_col[pos1]) / 2))
                # print("different? " + str(len(dict1_first_col[pos1]) -
                #                           lcs(dict1_first_col[pos1], dict2_first_col[pos2]) >
                #                           len(dict1_first_col[pos1]) / 2))
                if dict1_first_col[pos1].lower() == dict2_first_col[pos2].lower():
                    # print("Strings are EXACTLY equal.")
                    pos1 += 1
                    pos2 += 1
                elif dict1_first_col[pos1].lower() == dict2_first_col[pos2 + 1].lower():
                    # """Delete value at pos2 in dict2."""
                    # print("dict1[i] equals dict2[i+1]")
                    print("pop: " + str(pos2))
                    dict2.get(key).pop(pos2)
                    pos2 += 1
                elif dict1_first_col[pos1 + 1].lower() == dict2_first_col[pos2].lower():
                    """Insert "-" at pos2 in dict2."""
                    # print("dict1[i+1] equals dict2[i]")
                    # print('inserting "-" at ' + str(pos2) + ' in dict2')
                    dict2.get(key).insert(pos1, "-")
                    pos1 += 1
                elif len(dict1_first_col[pos1]) - lcs(dict1_first_col[pos1], dict2_first_col[pos2]) > \
                        len(dict1_first_col[pos1])/2:
                    """Not similar enough."""
                    # print("Not similar enough")
                    # try:
                    for i in range(1, len(dict1_first_col) - pos1):
                        """ASSUME that a matching string WILL be found at some index.
                        Matching defined as: differences being less than half of pivot string.
                        If matching string is not found, delete pos2 from dict2"""
                        # print(i)
                        # print("difference 1: " +
                        #       str(len(dict1_first_col[pos1+i]) - lcs(dict1_first_col[pos1+i], dict2_first_col[pos2])))
                        # print("half of dict1: " + str(len(dict1_first_col[pos1+i]) / 2))
                        # print("difference 2: " +
                        #       str(len(dict2_first_col[pos2+i]) - lcs(dict1_first_col[pos1], dict2_first_col[pos2+i])))
                        # print("half of dict2: " + str(len(dict2_first_col[pos2+i]) / 2))

                        if len(dict1_first_col[pos1+i]) - lcs(dict1_first_col[pos1+i], dict2_first_col[pos2]) < \
                                len(dict1_first_col[pos1+i])/2 - buffer:
                            """Insert element into dict2 at pos1."""
                            for j in range(i):
                                dict2.get(key).insert(pos1, "-")
                            pos1 += i
                            break
                        elif len(dict2_first_col[pos2+i]) - lcs(dict1_first_col[pos1], dict2_first_col[pos2+i]) < \
                                len(dict2_first_col[pos2+i])/2 - buffer:
                            """Delete element from dict2 at pos2."""
                            for k in range(i):
                                dict2.get(key).pop(pos2)
                            pos2 += i
                            break
                    # except IndexError:
                    #     # print("lolololol")
                    #     dict2.get(key).insert(pos2, "-")
                    #     pos2 += 1
                else:
                    """Strings are MOSTLY the same."""
                    # print("longest common subsequence of the two strings is ALMOST as long as dict[i]")
                    pos1 += 1
                    pos2 += 1
            dict1[key] = dict2.get(key)

    return dict1


def lcs(s1, s2):
    """
    Longest Common Sub-sequence (DP) from GeeksforGeeks

    :param s1: str
    :param s2: str
    :return: int, length of longest common sub-sequence
    """
    s1 = s1.lower()
    s2 = s2.lower()
    # find the length of the strings
    m = len(s1)
    n = len(s2)

    # declaring the array for storing the dp values
    grid = [[0] * (n + 1) for i in range(m + 1)]

    """Following steps build grid[m+1][n+1] in bottom up fashion 
    Note: grid[i][j] contains length of LCS of s1[0..i-1] 
    and s2[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                grid[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                grid[i][j] = grid[i - 1][j - 1] + 1
            else:
                grid[i][j] = max(grid[i - 1][j], grid[i][j - 1])

                # grid[m][n] contains the length of LCS of s1[0..n-1] & s2[0..m-1]
    return grid[m][n]


"""
End of file.
"""
