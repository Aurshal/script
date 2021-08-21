import requests
from bs4 import BeautifulSoup
import smtplib
import datetime
import os


class Scraper():
    total_notices = []
    sending_notices = []

    def scraping(self):
        self.total_notices = []
        print('Started web scraping')
        URL = 'https://exam.ioe.edu.np/'
        page = requests.get(URL)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find_all('tr')
            # print(table)
            for notices in table:
                notice_atag = notices.find('a')
                notice_name = notices.find('span')
                notice_date = notices.select('td:nth-child(3)')
                if(len(notice_date) == 1):
                    d = ((notice_date[0].text).split(', '))

                if notice_atag == None:
                    continue
                link_to_notice = URL+notice_atag['href']
                link = link_to_notice.replace(' ', '%20')

                self.total_notices.append((notice_name.text, d[1], link,))

        else:
            print('Server Error')

    def send_notice(self):
        mail_server = 'smtp.gmail.com'
        port = 587

        mail = smtplib.SMTP(mail_server, port)
        mail.ehlo()
        mail.starttls()
        mail.ehlo()

        sender = os.environ.get('sender')
        recipient = [x for x in (os.environ.get('receiver')).split(" ")]
        sender_pswd = os.environ.get('psd')
        mail.login(sender, sender_pswd)

        subject = '!NEW NOTICE ARRIVED FROM IOE!'
        body = self.sending_notices[0:]
        for i in body:
            xyz = f"{i[0]}\nDate: {i[1]}\nLink: {i[2]}"
            msg = f"Subject:{subject}\n\n{xyz}"
            mail.sendmail(sender, recipient, msg)
        sent = True
        mail.quit()


today = (datetime.datetime.now()).strftime("%B %d")
# while True:
data = Scraper()
data.scraping()
notices = data.total_notices
for notice in notices:
    if(notice[1] == today):
        data.sending_notices.append(notice)
    else:
        continue
if(len(data.sending_notices) > 0):
    data.send_notice()
else:
    print("No new notices to send")
