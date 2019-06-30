import AllFunctions as af
import gspread
import gspread_pandas
import json
from oauth2client.service_account import ServiceAccountCredentials
import time


# Use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret_key.json', scope)
client = gspread.authorize(creds)

# Create new spreadsheets only if they do not exist. Otherwise, open it.
spreadsheetName = "companyX"
try:
    print('NICE!!!')
    sh = client.open(spreadsheetName)
except gspread.exceptions.SpreadsheetNotFound:
    print('yikes')
    # Create spreadsheets in Google Drive.
    sh = client.create(spreadsheetName)
    time.sleep(1)
finally:
    print("No errors.")

# Share with yourself, or the sheet will remain inaccessible in this python script.
sh.share('mthane96@gmail.com',
         perm_type='user',
         role='writer')

# Share with client_email from json, or authentication errors will occur.
sh.share(json.load(open('secret_key.json'))["client_email"],
         perm_type='user',
         role='writer')

# Add a worksheet to spreadsheet
worksheetName = 'work1'
try:
    sh.add_worksheet(title=worksheetName, rows='10', cols='10')
except gspread.exceptions.APIError:
    deleteYN = input("A worksheet with that name already exists. Type 'y' to delete or 'n' to choose a new name: ")
    if deleteYN == 'y':
        sh.del_worksheet(worksheet=sh.worksheet(title=worksheetName))
    elif deleteYN == 'n':
        worksheetName = input('Enter new worksheet name: ')
        sh.add_worksheet(title=worksheetName, rows='10', cols='10')
    else:
        pass
finally:
    print("No errors.")

df = af.parse10k()

spread = gspread_pandas.Spread(json.load(open('secret_key.json'))["client_email"], spreadsheetName,
                               config=json.load(open('secret_key.json')))

spread.df_to_sheet(df=df, index=False, sheet='work1', start='A1', replace=True)
