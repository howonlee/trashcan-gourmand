import datetime
import email
import smtplib
import os
import random
from settings import Settings

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
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    random_root = "/home/howon/Dropbox/Projects/southcote"
    random_choices = [os.path.join(dp, f) for dp, dn, fn in os.walk(random_root) for f in fn]
    filtered_choices = list(filter(lambda x: x.endswith(".py"), random_choices))
    curr_choice = random.choice(filtered_choices)
    os.system("pygmentize -o {}/curr_img.png {}".format(curr_dir, curr_choice))
