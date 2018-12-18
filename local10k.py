import bs4

file = open('Companies/MSFT/msft-10k_20180630.htm')
soup = bs4.BeautifulSoup(file, 'html.parser')
attributeList = soup.select('a')

for i in range(len(attributeList)):
    # print(i)
    # print(attributeList[i])
    # print(attributeList[i].attrs)
    # # print(attributeList[i].attrs[0])
    # print(attributeList[i].attrs[1])
    for n in attributeList[i].attrs:
        # print(attributeList[i].attrs[n])
        if attributeList[i].attrs[n] == "BALANCE_SHEETS":
            print(attributeList[i].attrs[n])

