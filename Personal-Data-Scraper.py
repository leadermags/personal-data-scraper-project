#! python3
import requests
import pyperclip, bs4
import re
import sqlite3
import pandas as pd
import os

fileName = 'scraper_results.csv'
dbName = 'scraped-personal-data.db'
# Get current working directory to know where file will be saved
location = os.getcwd()

def main():

  print('This is your current working directory: ' + os.getcwd())
  try:
    print('Where would you like to save your file at? Please input the full path: ')
    location = input()
    os.chdir(location)
  except:
    print('You did not enter a valid path. File will be saved in current working directory.')

  # Connect to database
  conn = sqlite3.connect(dbName)
  # Allow database manipulation
  c = conn.cursor()

  try:
    # SQL query to create tables Links, Emails, Phones
    c.execute('''CREATE TABLE Links(ID INT, Link TEXT)''')
    c.execute('''CREATE TABLE Emails(ID INT, Link TEXT, Email TEXT)''')
    c.execute('''CREATE TABLE Phones(ID INT, Link TEXT, Phone TEXT)''')
    # Save created tables into database
    conn.commit()
  except:
    print('Tables already exists. Inserting more values...')

  # Uses clipboard to extract each link
  getLink()

  print('Do you want to save it into a CSV? ')
  saveToCSV = input()

  if (saveToCSV.lower() == 'yes'):

    # SQL query to first outputs all emails then phone numbers into CSV
    sql = """SELECT l.Link, e.Email, ''
          FROM Links l
          INNER JOIN Emails e ON l.Link = e.Link
          
          UNION ALL
          
          SELECT l.Link, '', p.Phone
          FROM Links l
          INNER JOIN Phones p ON l.Link = p.Link;"""
    
    # Use Pandas Module to allow write to CSV from database
    df = pd.read_sql_query(sql, conn)
    df.to_csv(fileName)

    print('Scraped Emails and Phone Numbers saved in CSV: ' + location + '\\' + fileName)

  else:
    print('Scraped Emails and Phone Numbers saved in database: ' + location + '\\' + dbName)

  # Close database
  conn.close()

# Extract links then calls other functions for each link in extracted links
def getLink():
  # Create a regex for webpages
  linkRegex = re.compile(r'''
  (http(s)?://                      # links starting with http:// or https://
  [a-zA-Z0-9_.+-/]+)      
  ''', flags=re.VERBOSE | re.I)

  # Extract links from clipboard
  copiedLinks = pyperclip.paste()
  extractedLinks = linkRegex.findall(copiedLinks)
  allLinks = []
  for l in extractedLinks:
    allLinks.append(l[0])           # only save link at index 0

  # Connect to database
  conn = sqlite3.connect(dbName)
  # Allow database manipulation
  c = conn.cursor()

  # i iterates for each ID number
  i = 1      
  for link in allLinks:

    # SQL query to insert each link into table Links
    c.execute('''INSERT INTO Links VALUES(?, ?)''', (i, link))
    
    # calls function to get the HTML source of each link
    getSource(link)
    
    # Get the text off the clipboard to pass into functions for scraping out the specified text
    copiedText = pyperclip.paste()
    extractedPhone = extractPhone(copiedText)
    extractedEmail = extractEmail(copiedText)

    # j iterates for each ID number for table Phones
    j = 1
    for phone in extractedPhone:
      # SQL query to insert current link and each phone number into table Phones
      c.execute('''INSERT INTO Phones VALUES(?, ?, ?)''', (j, link, phone))

    # j iterates for each ID number for table Emails
    j = 1
    for email in extractedEmail:
      # SQL query to insert current link and each email into table Emails
      c.execute('''INSERT INTO Emails VALUES(?, ?, ?)''', (j, link, email))

    i += 1

    # Save inserts into database
    conn.commit()

  return

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

main()