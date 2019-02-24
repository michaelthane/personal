import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from pprint import pprint
import json
import time

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret_key.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("AXP - American Express Company").sheet1

# Create spreadsheets in google drive
sh = client.create('test sheet')
time.sleep(1)

# Share with yourself, or the sheet will remain inaccessible in this python script
sh.share('mthane96@gmail.com',
         perm_type='user',
         role='writer')

# Share with client_email from json, or authentication errors will occur
with open('secret_key.json') as f:
    data = json.load(f)

sh.share(data["client_email"],
         perm_type='user',
         role='writer')

# Adding a sheet to spreadsheet
worksheet = sh.add_worksheet(title='work1', rows='100', cols='10')

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
#pprint(list_of_hashes)
