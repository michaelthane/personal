import bs4

exampleFile = open('msft-10k_20180630.htm')
exampleSoup = bs4.BeautifulSoup(exampleFile)
type(exampleSoup)
