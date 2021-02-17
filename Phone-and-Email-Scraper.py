#! python3
import requests
from pywebcopy import WebPage, elements, save_webpage
import pyperclip, bs4
import re
import openpyxl, os

def main():
  getLink()
  
  location = os.getcwd()
  print('Emails and Phone Numbers extracted. ')
  print('Data saved in ' + location + ' path.')

# Extract links
def getLink():
  # Create a regex for webpages
  linkRegex = re.compile(r'''

  (http(s)?://[a-zA-Z0-9_.+-/]+)      # links starting with http:// or https://

  ''', re.VERBOSE)

  copiedLinks = pyperclip.paste()
  extractedLinks = linkRegex.findall(copiedLinks)
  allLinks = []
  for l in extractedLinks:
    allLinks.append(l[0])
  wb = openpyxl.Workbook()
  sheet = wb.get_sheet_by_name('Sheet')
  sheet.title = 'All Links'

  i = 1
  for links in allLinks:
    cellNumber = 'A' + str(i)
    sheet[cellNumber] = str(links)
    wb.create_sheet(str(i))
    getSource(links, wb, str(i))
    i += 1
    wb.save('extractedData.xlsx')

# Copy text from links' html using bs4
def getSource(link, wb, sh):
  
  res = requests.get(str(link))
  res.raise_for_status()
  soup = bs4.BeautifulSoup(res.text, 'html.parser')
  elems = soup.select('body')
  pyperclip.copy(str(elems))
  extractInfo(link, wb, sh)

# Extract emails and phone numbers
def extractInfo(link, wb, sh):

  # Create a regex for phone numbers
  phoneRegex = re.compile(r'''
  # 000-000-0000, 000-0000, (000) 000-0000, 000-0000 ext 12345, ext. 12345, x12345
  (
  ((\d\d\d)|(\(\d\d\d\)))?            # area code (optional)
  (\s|-)                              # first seperator
  \d\d\d                              # second 3 digits
  -                                   # second seperator
  \d\d\d\d                            # last 4 digits
  (((ext(\.)?\s) | x)                 # word part for extention (optional)
  (\d{2,5}))?                         # number part for extension (optional)
  )
  ''', re.VERBOSE)

  # Create a regex for emails
  emailRegex = re.compile(r'''
  # some.+_thing@something.com

  [a-zA-Z0-9_.+-]+                 # name part
  @
  [a-zA-Z0-9_.+-]+                 # domain name

  ''', re.VERBOSE)

  # Get the text off the clipboard
  copiedText = pyperclip.paste()

  # Extract the email/phone from this text
  extractedPhone = phoneRegex.findall(copiedText)
  extractedEmail = emailRegex.findall(copiedText)
  allPhoneNumbers = []
  for phoneNumber in extractedPhone:
      allPhoneNumbers.append(phoneNumber[0])
  pasteText(allPhoneNumbers, extractedEmail, link, wb, sh)

# Input data into spreadsheet
def pasteText(allPhoneNumbers, extractedEmail, link, wb, sh):

  sheet = wb.get_sheet_by_name(sh)

  for j in range(0, len(extractedEmail)):
    cellNumber = 'A' + str(j + 1)
    sheet[cellNumber] = link

  i = 1
  for e in extractedEmail:
    cellNumber = 'B' + str(i)
    sheet[cellNumber] = str(e)
    i += 1

  i = 1
  for p in allPhoneNumbers:
    cellNumber = 'C' + str(i)
    sheet[cellNumber] = str(p)
    i += 1
    
  wb.save('extractedData.xlsx')

main()
