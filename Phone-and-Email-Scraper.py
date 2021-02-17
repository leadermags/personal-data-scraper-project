#! python3
import requests
from pywebcopy import WebPage, elements, save_webpage
import pyperclip, bs4
import re
import openpyxl, os

def main():
  print('Please copy the links onto your clipboard (Ctrl+C) before inputting file name.')

  print('What do you want to save your file as? ')
  fileName = input() + '.xlsx'

  getLink(fileName)

# Extract links
def getLink(fileName):
  # Create a regex for webpages
  linkRegex = re.compile(r'''

  (http(s)?://                      # links starting with http:// or https://
  [a-zA-Z0-9_.+-/]+)      

  ''', re.VERBOSE)

  copiedLinks = pyperclip.paste()
  extractedLinks = linkRegex.findall(copiedLinks)
  allLinks = []
  for l in extractedLinks:
    allLinks.append(l[0])           # only save link at index 0
  wb = openpyxl.Workbook()
  sheet = wb['Sheet']
  sheet.title = 'All Links'

  i = 1
  for link in allLinks:
    cellNumber = 'A' + str(i)
    sheet[cellNumber] = str(link)
    wb.create_sheet(str(i))
    text = getSource(link)
    
    # Get the text off the clipboard
    copiedText = pyperclip.paste()
    extractedPhone = extractPhone(copiedText)
    extractedEmail = extractEmail(copiedText)
    pasteText(extractedPhone, extractedEmail, link, wb, str(i))
    i += 1
    wb.save(fileName)

  if len(allLinks) != 0:
    location = os.getcwd()
    print('Emails and Phone Numbers extracted. ')
    print('Data saved in ' + location + '\\' + fileName)
  else:
    print('No links were found. No file created.')

# Copy text from links' html using bs4
def getSource(link):
  try:
    res = requests.get(str(link))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('body')
    return pyperclip.copy(str(elems))
  except:
    print('Could not get ' + link)
  
def extractPhone(copiedText):
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
  extractedPhone = phoneRegex.findall(copiedText)
  
  allPhoneNumbers = []
  for phoneNumber in extractedPhone:
      allPhoneNumbers.append(phoneNumber[0])    # only saves phone number at index 0

  return allPhoneNumbers

def extractEmail(copiedText):
  
  # Create a regex for emails
  emailRegex = re.compile(r'''
  # some.+_thing@something.com

  [a-zA-Z0-9_.+-]+                 # name part
  @
  [a-zA-Z0-9_.+-]+                 # domain name

  ''', re.VERBOSE)
  extractedEmail = emailRegex.findall(copiedText)
  return extractedEmail

# Input data into spreadsheet
def pasteText(allPhoneNumbers, extractedEmail, link, wb, sh):

  sheet = wb[sh]

  for j in range(0, len(extractedEmail) + len(allPhoneNumbers)):
    cellNumber = 'A' + str(j + 1)
    sheet[cellNumber] = link

  i = 1
  for e in extractedEmail:
    cellNumber = 'B' + str(i)
    sheet[cellNumber] = str(e)
    i += 1

  for p in allPhoneNumbers:
    cellNumber = 'C' + str(i)
    sheet[cellNumber] = str(p)
    i += 1

main()
