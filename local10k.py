import bs4


def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


file = open('Companies/MSFT/msft-10k_20180630.htm')
exampleFile = open('C:/Users/mthan/PycharmProjects/Automating the Boring Stuff/example.html')
# exampleFile = open('Automating the Boring Stuff/example.html')



soup = bs4.BeautifulSoup(exampleFile, 'html.parser')
plist = soup.select('p')

alist = []

for p in plist:
    print(p.select('a'))
    if p.select('a') != []:
        alist.append(p.select('a'))
print(alist)

for i in alist:
    print(i)
#attributeList = soup.select('tr')[0].select('td')

# list1 = []
# list2 = []
#
# print(attributeList[0].text.strip('\n'))
#
# # attributeList[0].text.strip('\n')
#
#
# # Strip newline
# for i in range(len(attributeList)):
#     list1.append(attributeList[i].text.strip('\n'))
#
# print(list1)
#
# # Replace commas with empty string
# for i in range(len(list1)):
#     list2.append(list1[i].replace(',', ''))
#
# #print(list2)
#
# list3 = []
#
# for data in list2:
#     # print(data)
#     if data == 'Total assets' or isNumber(data):
#         list3.append(data)
#
# print(list3)



# print(len(attributeList))
#
# datacells = attributeList[0].select('td')
#
# print(datacells[0].text)
#
# print(len(datacells))


# for i in range(len())


#print(attributeList[0].text)


#for i in range(len(attributeList)):
#    print(i)
    # print(attributeList[i].select('table'))
    #if attributeList[i].select('table'):
    #    print(i)
    #if attributeList[i].get('name') == 'BALANCE_SHEETS':
    #    print(attributeList[i])
    # print(attributeList[i].get('name'))
    #if attributeList[i].test == 'Balance Sheets'
    # print(attributeList[i])
    # print(attributeList[i].attrs)
    # # print(attributeList[i].attrs[0])
    # print(attributeList[i].attrs[1])
    # for n in attributeList[i].attrs:
    #     # print(attributeList[i].attrs[n])
    #     if attributeList[i].attrs[n] == "BALANCE_SHEETS":
    #         print(attributeList[i].attrs[n])
    # print(attributeList[i])
