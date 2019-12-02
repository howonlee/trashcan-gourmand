import datetime
import email
import smtplib
import os
import random
import functools
from settings import Settings
from typing import List, Union

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

def set_curr_res(settings: Settings) -> None:
    """ Mutates curr_res.html in current folder """
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    random_root = settings.root_dir
    curr_choice = choose_random_file(random_root, settings.filetypes)
    os.system("pygmentize -o {}/curr_res.html {}".format(curr_dir, curr_choice))

def choose_random_file(random_root: str, filetypes: Union[str, List[str]]) -> str:
    random_choices = [os.path.join(dp, f) for dp, dn, fn in os.walk(random_root) for f in fn]
    filter_func = functools.partial(filter_by_filetype, filetypes=filetypes)
    filtered_choices = list(filter(filter_func, random_choices))
    return random.choice(filtered_choices)

def filter_by_filetype(member: str, filetypes: Union[str, List[str]]):
    if type(filetypes) == str:
        return member.endswith(filetypes)
    elif type(filetypes) == list:
        for filetype in filetypes:
            if member.endswith(filetype):
                return True
        return False
    else:
        raise Exception("Wrong type on filetype")

