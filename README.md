# Personal Data Web Scraper

Goes through the copied links then extracts any emails, phone numbers, and SSN from each link that was copied then paste into an Excel workbook.

Project started off with one of Al Sweigart's [*Automate the Boring Stuff with Python*](https://automatetheboringstuff.com/2e/chapter7/) projects. Then I got inspired to incorporate other ways to automate and track the amount of emails and phone numbers found on websites.

There is also a .bat file template to allow you to run the script using Windows+R.

I would like to expand this project to extract other personal data.

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

This allows you to run the Python script using the Windows+R command. The instructions I followed are from [*Automate the Boring Stuff*](https://automatetheboringstuff.com/2e/appendixb/).

Using the template Personal-Data-Scraper.bat, edit the file path to match your own file path of where the Python script is saved then save the Bat file in the same folder as the script.

On Windows, go to Control Panel > System and Security > System > Advanced system settings > Environment Variables.

Then select 'Path' in the 'System variables' box > Edit > New.

Input the full file path to where the Python script and Bat file are.
