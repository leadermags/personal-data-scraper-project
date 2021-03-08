# Personal Data Web Scraper

This is a Python script that goes through the copied links then scrapes any emails and phone numbers from each link that was copied onto the clipboard, then paste those data into an Excel workbook. This is for anyone or any organizations that do not want private emails to readily available to the public. From my internship experience, I learned about the risks that follow a successful phishing attack. By limiting private email addresses found on public webpages and have a group email instead can deter targeted phishing attacks.

On the saved Excel workbook, the first sheet will be a list of all the links that was found in the copied text in your clipboard. The subsequent sheets correlate to the data scraped for which row of the first sheet, 'All Links'. In the subsequent sheets:
- Column A - Link Address
- Column B - Email Address(es)
- Column C - Phone Number(s)

There is also a .bat file template to allow you to run the script using Windows+R.

I would like to expand this project to extract other personal data.

The project started off with one of Al Sweigart's [*Automate the Boring Stuff with Python*](https://automatetheboringstuff.com/2e/chapter7/) projects. Then I got inspired to incorporate other ways to automate and track the amount of emails and phone numbers found on websites. 

## Installing the modules used in this script:

Before running the following powershell commands, change your current working directory to where you've installed pip.exe (usually this is in Scripts in your Pythons folder).

Requests Module - HTTP library
  `pip.exe install requests`

Pyperclip Module - use clipboard for copy and paste
   `pip.exe install pyperclip`

Beautiful Soup Module - HTML parser
   `pip.exe install beautifulsoup4`

Openpyxl Module - creates and edits Excel workbooks
   `pip.exe install openpyxl`

## Setting up PATH environmental variable:

This allows you to run the Python script using the Windows+R command. The instructions I followed are from [*Automate the Boring Stuff with Python*](https://automatetheboringstuff.com/2e/appendixb/).

Using the template Personal-Data-Scraper.bat, edit the file path to match your own file path of where the Python script is saved then save the Bat file in the same folder as the script.

On Windows, go to Control Panel > System and Security > System > Advanced system settings > Environment Variables.

Then select 'Path' in the 'System variables' box > Edit > New.

Input the full file path to where the Python script and Bat file are.
