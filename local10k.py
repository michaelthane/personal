import AllFunctions as af
import os
import bs4

# Create list of file names in directory.

# for filename in os.listdir('Companies/MSFT'):
#     filePath = 'Companies/MSFT' + '/' + filename
#     print('Companies/MSFT' + '/' + filename)

# print(af.parse10k('Companies/MSFT/msft-10k_20180630.htm'))
# print(af.parse10k('Companies/MSFT/msft-10k_20170630.htm'))


# implement code to look for page break
# only start recording when on balance sheets page, reset when new page break occurs



# check if line if a<>
#print(open('Companies/MSFT/msft-10k_20180630.htm').read())

msft = open('Companies/MSFT/msft-10k_20180630.htm')

data = msft.readlines()

msft.close()

soup = bs4.BeautifulSoup("".join(data), features='lxml')

print(soup)

#soup.

# print(soup)

# soup.


# f = open('tempFile.txt', 'w')
# for i in range(100):
#     f.write(msft.readline())


