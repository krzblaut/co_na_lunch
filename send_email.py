import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os 
from make_html import CreateHTML

# recipients = ['maciej.ferszt@3pplus.de', 
#               'artur.potrzebny@3pplus.de', 
#               'mateusz.hycz@3pplus.de', 
#               'krzysztof.blaut@3pplus.de',
#               ]

recipients = ['krzblaut@gmail.com',
              'krsajdok@gmail.com',
              ]

load_dotenv()
username = os.getenv('ONET_USER')
password = os.getenv('ONET_PASSWORD')


# Set up the email message
msg = MIMEMultipart()
msg['From'] = 'co.na.lunch@buziaczek.pl'
msg['To'] = ', '.join(recipients)
msg['Subject'] = 'Co na lunch byku'


html = CreateHTML()
body = html.generate()
msg.attach(MIMEText(body, 'html'))


# Connect to the SMTP server
smtp_server = 'smtp.poczta.onet.pl'
smtp_port = 25
smtp_username = username
smtp_password = password


server = smtplib.SMTP(smtp_server, smtp_port)
print('initialized server')
server.starttls()
print('started tls')
server.login(smtp_username, smtp_password)
print('logged in')
# Send the email
server.sendmail(smtp_username, msg['To'], msg.as_string())
server.quit()
