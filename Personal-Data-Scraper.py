#! python3
import requests
import pyperclip, bs4
import re
import sqlite3
import pandas as pd
import os

fileName = 'scraper_results.csv'
dbName = 'scraped-personal-data.db'
location = os.getcwd()

def main():
  conn = sqlite3.connect(dbName)
  c = conn.cursor()

  # c.execute('''CREATE TABLE emailsAndPhones(date DATE, link TEXT, email TEXT, phone TEXT)''')
  c.execute('''CREATE TABLE Links(ID INT, Link TEXT)''')
  c.execute('''CREATE TABLE Emails(ID INT, Link TEXT, Email TEXT)''')
  c.execute('''CREATE TABLE Phones(ID INT, Link TEXT, Phone TEXT)''')
  
  conn.commit()

  getLink()

  print('Do you want to save it into a CSV? ')
  saveToCSV = input()

  if (saveToCSV.lower() == 'yes'):
      
    sql = """SELECT l.Link, e.Email, ''
          FROM Links l
          INNER JOIN Emails e ON l.Link = e.Link
          
          UNION ALL
          
          SELECT l.Link, '', p.Phone
          FROM Links l
          INNER JOIN Phones p ON l.Link = p.Link;"""
    
    df = pd.read_sql_query(sql, conn)

    df.to_csv(fileName)

    print('Scraped Emails and Phone Numbers saved in CSV: ' + location + '\\' + fileName)

  else:
    print('Scraped Emails and Phone Numbers saved in database: ' + location + '\\' + dbName)

  conn.close()

# Extract links then calls other functions for each link in extracted links
def getLink():
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

  conn = sqlite3.connect('scraped-personal-data.db')
  c = conn.cursor()

  # i iterates for each cell number
  i = 1      
  for link in allLinks:

    c.execute('''INSERT INTO Links VALUES(?, ?)''', (i, link))
    
    # calls function to get the HTML source of each link
    getSource(link)
    
    # Get the text off the clipboard to pass into functions for scraping out the specified text
    copiedText = pyperclip.paste()
    extractedPhone = extractPhone(copiedText)
    extractedEmail = extractEmail(copiedText)

    j = 1
    try:
      for phone in extractedPhone:
        c.execute('''INSERT INTO Phones VALUES(?, ?, ?)''', (j, link, phone))
    except:
      c.execute('''INSERT INTO Phones VALUES(?, ?, ?)''', (j, link, 'null'))
    
    j = 1
    try: 
      for email in extractedEmail:
        c.execute('''INSERT INTO Emails VALUES(?, ?, ?)''', (j, link, email))
    except:
      c.execute('''INSERT INTO Emails VALUES(?, ?, ?)''', (j, link, 'null'))

    i += 1

    conn.commit()

  return
  # checks if there were any links that could be found in clipboard
  # if len(allLinks) != 0:
  #   return True
    
  # else:
  #   return False 

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