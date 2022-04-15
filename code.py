# importing the urllib library for creating the connection with the web
# importing the regualar expression library for string extraction
# importing the ssl library for certificate verification

import urllib.request
import urllib.parse
import urllib.error
import re
import ssl
import pandas as pd

# getting the beautifulsoup lib for html parsing
from bs4 import BeautifulSoup

# ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    # asking user for url to scrape
    url = input("Enter the URL: ")

    # getting the html content of the url and storing it the "html" variable
    html = urllib.request.urlopen(url, context=ctx).read()

    # creating the beautiful soup object for parsing
    soup = BeautifulSoup(html, 'html.parser')

    # getting all the html tag
    p = soup.find_all('div', class_="catbox")

    # creating an empty list
    emails = []

    # Iterate over all tags and find emails from the paragraph by using regular expression
    for item in p:
        para = item.p.text.strip()
        email = re.search('\S+@\S+', para)
        if email is not None:
            email = email.group()
            emails.append(email[0:len(email)-1])

    if not emails:
        print("No Email found")
    else:
        print("Total Emails Found:", len(emails))
        data = {"emails": emails}
        # creatung pandas data frame and saving the emails in csv file
        df = pd.DataFrame(data)
        # print(df)
        # saving emails to csv file
        df.to_csv('emails.csv')
except Exception as e:
    print(e)
