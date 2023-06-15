import smtplib
import ssl
import os

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "lyssa.flynn@gmail.com" #Should I hide my e-mail as well?
    password = os.getenv("PASSWORD") #How to implement system environment on github?

    receiver = "lyssa.flynn@gmail.com" #Should I hide my e-mail as well?
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
