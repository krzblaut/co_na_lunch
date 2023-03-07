from drukarnia import DrukarniaMenu
from send_email import MailSender


import datetime

if __name__ == '__main__':
    
    now = datetime.datetime.now()

    if now.hour < 10:
        druk = DrukarniaMenu()
        druk.login()
        druk.send_message()
    else:
        sender = MailSender()
        sender.send_email()
        

