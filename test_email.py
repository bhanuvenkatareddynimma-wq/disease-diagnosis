import smtplib
from email.message import EmailMessage

def test_email():
    sender_email = "d31520052@gmail.com"
    app_password = "nngizedyzdilvdze"
    receiver_email = "d31520052@gmail.com"

    subject = "⚠️ Test Health Alert"
    body = "Test body message."

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print("Success!")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test_email()
