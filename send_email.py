import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os 
from make_html import CreateHTML


class MailSender:

    recipients = ['maciej.ferszt@3pplus.eu', 'artur.potrzebny@3pplus.eu', 'mateusz.hycz@3pplus.eu', 'krzysztof.blaut@3pplus.eu',]


    def __init__(self):
        load_dotenv()
        self.smtp_server = 'smtp.poczta.onet.pl'
        self.smtp_port = 25
        self.smtp_username = os.getenv('ONET_USER')
        self.smtp_password = os.getenv('ONET_PASSWORD')
        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()
        self.server.login(self.smtp_username, self.smtp_password)


    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = 'co.na.lunch@buziaczek.pl'
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = 'Co na lunch wariacie?'
        html = CreateHTML()
        body = html.generate()
        msg.attach(MIMEText(body, 'html'))
        self.server.sendmail(self.smtp_username, self.recipients, msg.as_string())
        self.server.quit()








# Set up the email message

