import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import email.utils

def test_email_robust():
    sender_email = "d31520052@gmail.com"
    app_password = "nngizedyzdilvdze"
    receiver_email = "d31520052@gmail.com"

    subject = "Test Robust Email"
    body = "Checking if Date and Message-ID fix anti-spam drops."

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid()

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print("Success sending robust email!")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test_email_robust()
