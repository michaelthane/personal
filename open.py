#! python3
# mapIt.py - Launches an SEC edgar search in the browser using a ticker from the
# command line or clipboard.

import webbrowser, sys, pyperclip

# Run from cmd line: python edgar.py <ticker>
if len(sys.argv) > 1:
    # Get ticker from command line.
    ticker = ' '.join(sys.argv[1:])
else:
    # Get ticker from clipboard.
    ticker = pyperclip.paste()

webbrowser.open('https://www.sec.gov/cgi-bin/browse-edgar?CIK='+ticker+'&owner=exclude&action=getcompany')
