import bs4

file = open('example.html')

# Need to specify which parser to use...
# # html.parser will work on .htm files
soup = bs4.BeautifulSoup(file, 'html.parser')
print(type(soup))
elems = soup.select('#author')
print(type(elems))
print(len(elems))
print(type(elems[0]))
print(elems[0].getText())
print(str(elems[0]))
print(elems[0].attrs)
