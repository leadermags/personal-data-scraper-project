#! python3
import requests
import pyperclip, bs4
import re
import openpyxl, os

def main():
  print('Please copy the links onto your clipboard (Ctrl+C) before inputting file name.')
  print('This is your current working directory: ' + os.getcwd())
  try:
    print('Where would you like to save your file at? Please input the full path: ')
    location = input()
    os.chdir(location)
  except:
    location = os.getcwd()
    print('You did not enter a valid path. File will be saved in current working directory.')

  print('What name do you want to save your file as? ')
  fileName = input() + '.xlsx'

  # return a boolean
  didCreateFile = getLink(fileName)

  if(didCreateFile):
    print('Any Emails and Phone Numbers are extracted. ')
    print('Data saved in ' + location + '\\' + fileName)
  else:
    print('No links were found. No file created.')

# Extract links then calls other functions for each link in extracted links
def getLink(fileName):
  # Create a regex for webpages
  linkRegex = re.compile(r'''
  (http(s)?://                      # links starting with http:// or https://
  [a-zA-Z0-9_.+-/]+)      
  ''', flags=re.VERBOSE | re.I)

  # extract links from clipboard
  copiedLinks = pyperclip.paste()
  extractedLinks = linkRegex.findall(copiedLinks)
  allLinks = []
  for l in extractedLinks:
    allLinks.append(l[0])           # only save link at index 0
  
  # creates a new Excel workbook
  wb = openpyxl.Workbook()
  sheet = wb['Sheet']

  sheet.title = 'All Links'

  # i iterates for each cell number
  i = 1      
  for link in allLinks:
    cellNumber = 'A' + str(i)
    sheet[cellNumber] = str(link)
    
    # each corresponding row for links on this sheet will correspond to the other sheet's name
    wb.create_sheet(str(i))

    # calls function to get the HTML source of each link
    getSource(link)
    
    # Get the text off the clipboard to pass into functions for scraping out the specified text
    copiedText = pyperclip.paste()
    extractedPhone = extractPhone(copiedText)
    extractedEmail = extractEmail(copiedText)

    # calls function to paste extracted text into spreadsheet
    pasteText(extractedPhone, extractedEmail, link, wb, str(i))

    i += 1
    wb.save(fileName)

  # checks if there were any links that could be found in clipboard
  if len(allLinks) != 0:
    return True
    
  else:
    return False

# Copy text from links' html using bs4
def getSource(link):

  # error handling if source HTML could not be retrieved
  try:
    res = requests.get(str(link))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('body')
    return pyperclip.copy(str(elems))
  except:
    print('ERROR: Could not get ' + link)
 
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

  ''', flags=re.VERBOSE | re.I)

  extractedEmail = emailRegex.findall(copiedText)

  return extractedEmail

# Input data into spreadsheet
def pasteText(allPhoneNumbers, extractedEmail, link, wb, sh):

  # wb stands for workbook, and sh stands for current sheet name
  sheet = wb[sh]

  # pastes the same link for every email, phone number, and SSN found
  for j in range(0, len(extractedEmail) + len(allPhoneNumbers)):
    cellNumber = 'A' + str(j + 1)
    sheet[cellNumber] = link

  # i iterates each cell number
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
