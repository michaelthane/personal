import bs4

file = open('Companies/MSFT/msft-10k_20180630.htm')
soup = bs4.BeautifulSoup(file, 'html.parser')
attributeList = soup.select('a')

for i in range(len(attributeList)):
    print(i)
    print(attributeList[i])
    print(attributeList[i].attrs)
    print(attributeList[i].attrs.values())

