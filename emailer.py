import datetime
import email
import smtplib
from settings import Settings
from ansi2html import Ansi2HTMLConverter

def send_message(contents: str, date: datetime.date, settings: Settings) -> None:
    msg_obj: email.message.EmailMessage = email.message.EmailMessage()
    msg_obj['From'] = settings.smtp_username
    msg_obj['To'] = settings.smtp_dest_email
    msg_obj['Subject'] = "Trashcan Gourmand | {}".format(str(date))
    msg_obj.set_content(contents)
    with smtplib.SMTP(settings.smtp_url, settings.smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg_obj)

if __name__ == "__main__":
    converter = Ansi2HTMLConverter()
    randfile = 
    pass
