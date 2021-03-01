import requests
from bs4 import BeautifulSoup
import smtplib
import time
import getpass


class Scraper():
    total_notices = []

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
                if notice_atag == None:
                    continue
                link_to_notice = URL+notice_atag['href']
                link = link_to_notice.replace(' ','%20')
                # print(notice_name.text)
                # print(link)
                
                self.total_notices.append((notice_name.text,link))

        else:
            print('Server Error')

    def send_notice(self):
        mail_server = 'smtp.gmail.com'
        port = 587

        mail = smtplib.SMTP(mail_server,port)
        mail.ehlo()
        mail.starttls()
        mail.ehlo()
        

        sender = 'mraurshal@gmail.com'
        recipient = 'kushalsubedi2@gmail.com'
        # sender_pswd = getpass.getpass(prompt='PASSWORD:')
        mail.login(sender, '2058@kus')

        subject = '!NEW NOTICE ARRIVED FROM IOE!'
        body = self.total_notices[0:3]
        msg = f"Subject:{subject}\n\n{body}"
        mail.sendmail(sender,recipient,msg)
        mail.quit()

    

while True:
    data = Scraper()
    data.scraping()
    notices  =  data.total_notices
    x = len(notices)
    print(x)
    time.sleep(3)
    print('for y')
    new_data = Scraper()
    # data.total_notices = []
    new_data.scraping()
    new_notices  =  new_data.total_notices
    y = len(new_notices)
    print(y)


    if y == (x):
        print('no new notices found')
        # data.send_notice()
        # print('MAIL sent successfully')
        
    else:
        print('notices found')
        data.send_notice()
        print('MAIL sent successfully')


    











    