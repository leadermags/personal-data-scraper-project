# ***Need to Update***

# Implementation

- main() method calls on getLink() method
  - getLink() method scraps all the links copied onto clipboard then calls on getSource(), extractPhone(), extractEmail(), extractSSN(), and pasteText() methods
    - takes in fileName as the parameter
    - returns True or False
    - getSource() method parses out source HTML for each link
      - takes in link as the parameter
    - extractPhone() method scrapes out phone numbers
      - takes in copied text from getSource() method as the parameter
      - returns extracted phone numbers
    - extractEmail() method scrapes out emails
      - takes in copied text from getSource() method as the parameter
      - returns extracted emails
    - extractSSN() method scrapes out SSN
      - takes in copied text from getSource() method as the parameter
      - returns extracted phone numbers
    - pasteText() method pastes the text onto an Excel workbook
      - takes in each of the extracted data from earlier methods as well as the current link, workbook, and sheet currently working on

# High-Level Flowchart

![high-level flowchart](https://github.com/leadermags/personal-data-scraper-project/blob/main/img/personal-data-scraper-flowchart.png?raw=true)
