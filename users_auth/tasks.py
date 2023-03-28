from celery import shared_task

import smtplib

@shared_task(bind=True)
def send_mail(self,sender, recipient, headers, body):
    SMTP_SERVER='smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_PASSWORD = 'almfxpywqlsazypo'
    session = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender,SMTP_PASSWORD)
    send_it = session.sendmail(sender, recipient, headers + "\r\n\r\n" +  body)
    print("send the mail")
    session.quit()
