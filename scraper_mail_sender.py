import requests # http requests

from bs4 import BeautifulSoup # web scraping

# send the mail
import smtplib

# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# system date and time manipulation
from datetime import datetime

import os
from dotenv import load_dotenv
from pathlib import Path

# load variables from .env file
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
MY_EMAIL = os.getenv('MY_EMAIL')
MY_EMAIL_PASSWORD = os.getenv('MY_EMAIL_PASSWORD')
MY_GOOGLE_EMAIL_APP_PASSWORD = os.getenv('MY_GOOGLE_EMAIL_APP_PASSWORD')



def showTime():
    return str("["+datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')+" UTC]")


def pause():
    programPause = input("Press the <ENTER> key to continue...")


# email content placeholder

content = ''


#extracting Hacker News Stories


def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+ '<a href="' + tag.a.get('href') + '">' + tag.text + '</a>' + "\n" + '<br>') if tag.text!='More' else '')
        #print(tag.prettify) #find_all('span',attrs={'class':'sitestr'}))
    return(cnt)
    
    
if __name__ == "__main__":    
    cnt = extract_news('https://news.ycombinator.com/')
    content += cnt
    content += ('<br>------<br>')
    content +=('<br><br>End of Message')


    #lets send the email

    print('Composing Email...')

    # update your email details
    # make sure to update the Google Low App Access settings before

    SERVER = 'smtp.gmail.com' # "your smtp server"
    PORT = 587 # your port number
    FROM = MY_EMAIL # "your from email"
    GOOGLE_APP_PASSWORD = MY_GOOGLE_EMAIL_APP_PASSWORD # myaccount.google.com/apppasswords
    TO = 'adolfhitler@gmail.com' # "recipient email id"  # can be a list
    print(FROM)
    print(GOOGLE_APP_PASSWORD)
   

    # fp = open(file_name, 'rb')
    # Create a text/plain message
    # msg = MIMEText('')
    msg = MIMEMultipart()

    # msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
    msg['Subject'] = '[Automated Email] Top News Stories HN ' + str(showTime())
    msg['From'] = FROM
    msg['To'] = TO

    msg.attach(MIMEText(content, 'html'))
    # fp.close()

    print('Initiating Server...')

    server = smtplib.SMTP(SERVER, PORT)
    #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    #server.ehlo
    server.login(FROM, GOOGLE_APP_PASSWORD)
    server.sendmail(FROM, TO, msg.as_string())

    print('Email Sent...')

    server.quit()






