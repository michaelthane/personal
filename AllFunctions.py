"""
Creator: Michael Thane
Last Revised: 3/4/2019
Description: This library contains any and all functions used throughout this application.
             This will improve readability and organization.
"""

import bs4
from dateutil.parser import parse
import pandas as pd


# Determine if string is a number
def is_number(string):
    """
    Return whether the string can be interpreted as a number.
    
    :param string: str, string to check for number
    :return: bool
    """
    exclusions = [',', '$', '(', ')']
    try:
        for x in exclusions:
            float(string.replace(x, ''))
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


def get_values(analyzingValue, tags):
    """
    Return a list ...
    Get list of values indicated by analyzingValue.
    When using is_number(), remove unicode in string.

    :param analyzingValue: 
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
            if data.text.strip('\n') == analyzingValue and data.text.strip('\n') not in return_set:
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


def parse10k(file_path):
    """
    Return a dataframe of values from input file.
    
    :param file_path:  str, path of file.
    :return: pandas.DataFrame()
    """
    soup = bs4.BeautifulSoup(open(file_path), 'html.parser')

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
    num_cols = 0  # THIS CANNOT BE HARDCODED!!!
    col_lens = []
    for elem in soup.stripped_strings:

        # Starting with the date, the first row will be the col names, except for the unit (in millions) and '$'
        #if elem in exclusions:
        #    continue  # Go to the next loop iteration
        if pos == 0:
            if not is_date(elem, fuzzy=True) or elem in exclusions:
                continue
            else:
                # First elem should be a date like 'June 30' or similar.
                table[elem] = []  # key = elem : value = list
                col_names.append(elem)
                num_cols += 1
                pos += 1
        elif elem == "$" or elem == ")":
            continue
        elif is_number(elem) and pos < num_cols + 1:
            # These elems should be years like '2018' or '2017' or similar.
            table[elem] = []
            col_names.append(elem)
            pos += 1
            num_cols += 1
        # elif (elem[0] == "$" or elem[:3] == "and") and len(elem) > 1:
        #    # If description column has numeric values, include them in description.
        #    table.get(col_names[0])[-1] += elem
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

            # If an element has been added to a column out of order, fill remaining columns with hyphens.
            # if (pos % num_cols) != 0 and (len(table.get(col_names[0])) > len(table.get(col_names[1])) or
            #                               len(table.get(col_names[0])) > len(table.get(col_names[2]))):
            #     for i in range((len(table.get(col_names[0])) - len(table.get(col_names[1]))) - 1):
            #         table.get(col_names[1]).append("-")
            #         pos += 1
            #
            #     for i in range((len(table.get(col_names[0])) - len(table.get(col_names[2]))) - 1):
            #         table.get(col_names[2]).append("-")
            #         pos += 1
            pos += 1
        elif is_number(elem) and pos > num_cols:
            # Put financial value in appropriate position.
            table.get(col_names[pos % num_cols]).append(elem)
            pos += 1

    for pair in table:
        print(len(table.get(pair)))
    print()

    for i in range(1, len(col_names)):
        if len(table.get(col_names[0])) > len(table.get(col_names[i])):
            for j in range((len(table.get(col_names[0])) - len(table.get(col_names[i])))):
                table.get(col_names[i]).append("-")

    # if len(table.get(col_names[0])) > len(table.get(col_names[1])):
    #     for i in range((len(table.get(col_names[0])) - len(table.get(col_names[1])))):
    #         table.get(col_names[1]).append("-")
    # if len(table.get(col_names[0])) > len(table.get(col_names[2])):
    #     for i in range((len(table.get(col_names[0])) - len(table.get(col_names[2])))):
    #         table.get(col_names[2]).append("-")

    for key in table:
        print(key)
        print(len(table.get(key)))

    return pd.DataFrame(data=table)


"""
End of file.
"""
