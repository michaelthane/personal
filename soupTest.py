# The requests module lets you easily
# download files from the Web.
import requests
import bs4

# requests.get() takes a string URL to download
# Return a "Response" object

# <response>.status_code == requests.codes.ok == 200
# means every thing went fine

# <response>.text return text

# <response>.raise_for_status() will raise any errors
# good way to ensure that a program halts
# if a bad download occurs
# wrap with try and except statements

# <response>.iter_content(<number of bytes>)
# 100000 BYTES (100kb) is generally good

