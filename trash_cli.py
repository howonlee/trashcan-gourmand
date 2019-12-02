#!/usr/bin/env python3.7
import os
import time
import datetime
import crontab
import click
from typing import Union, List, Dict, Any
import email
import smtplib
import random
import functools
import dataclasses
import json


@dataclasses.dataclass
class Settings(object):
    root_dir: str # Root dir to sample the files from
    filetypes: Union[str, List[str]] # filetype or filetypes to sample from
    smtp_username: str
    smtp_password: str
    smtp_dest_email: str
    smtp_url: str = "smtp.gmail.com"
    smtp_port: int = 587

    def to_file(self, settings_filename: str) -> None:
        with open(settings_filename, "w") as settings_file:
            json.dump(dataclasses.asdict(self), settings_file)

    @staticmethod
    def from_file(settings_filename: str):
        with open(settings_filename, "r") as settings_file:
            json_res: Dict[str, Any] = json.load(settings_file)
            return Settings(**json_res)

def get_message() -> str:
    """
    Depends upon filesystem state to get the message
    """
    curr_dir = get_settings_dir()
    res = ""
    with open("{}/curr_res.html".format(curr_dir), "r") as curr_file:
        res = curr_file.read()
    return res


def set_curr_res(settings: Settings) -> None:
    """ Mutates curr_res.html in current folder """
    curr_dir = get_settings_dir()
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

def get_settings_dir() -> str:
    """
    Side effect of making sure the settings dir exists
    """
    res = os.path.expanduser("~/.trashcangourmand")
    # Make sure it actually exists
    os.makedirs(res, exist_ok=True)
    return res

def get_settings_filename() -> str:
    return "{}.settings".format(str(int(time.time())))

def get_settings_path() -> str:
    return os.path.join(get_settings_dir(), get_settings_filename())


def get_all_settings() -> List[Settings]:
    res: List[Settings] = []
    settings_filenames = filter(
            lambda x: x.endswith("settings"),
            os.listdir(get_settings_dir())
            )
    settings_paths = [os.path.join(get_settings_dir(), fn) for fn in settings_filenames]
    return list(map(Settings.from_file, settings_paths))

def process_filetypes(filetypes: str) -> Union[str, List[str]]:
    if "," not in filetypes:
        return filetypes
    else:
        return list(map(lambda x: x.strip(), filetypes.split(",")))

def send_message(contents: str, date: datetime.date, settings: Settings) -> None:
    msg_obj: email.message.EmailMessage = email.message.EmailMessage()
    msg_obj['From'] = settings.smtp_username
    msg_obj['To'] = settings.smtp_dest_email
    msg_obj['Subject'] = "Trashcan Gourmand | {}".format(str(date))
    msg_obj.set_content(contents)
    msg_obj.add_alternative(contents, subtype='html')
    with smtplib.SMTP(settings.smtp_url, settings.smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg_obj)

@click.group()
def cli():
    pass

@cli.command()
def setsettings():
    settings_path = get_settings_path()
    root_dir = os.path.expanduser(input("Root dir (the root dir of the project to email > "))
    filetypes = process_filetypes(input("Filetypes (the filetypes to email): separated by commas. For example, .py,.js > "))
    smtp_username = input("SMTP username (your webmail username, usually) > ")
    smtp_password = input("SMTP app password (for gmail, see https://support.google.com/accounts/answer/185833) > ")
    smtp_dest_email = input("Destination email. Can be same or different from SMTP username. > ")
    smtp_url = input("SMTP url [smtp.gmail.com] > ") or "smtp.gmail.com"
    smtp_port = input("SMTP port [587] > ") or 587
    new_settings = Settings(root_dir=root_dir,
            filetypes=filetypes,
            smtp_username=smtp_username,
            smtp_password=smtp_password,
            smtp_dest_email=smtp_dest_email,
            smtp_url=smtp_url,
            smtp_port=int(smtp_port))
    new_settings.to_file(settings_path)
    click.echo("New settings saved.")
    click.echo("Now go run trashcangourmand setcron")
    click.echo("Or go run trashcangourmand dish")

@cli.command()
def dish():
    all_settings = get_all_settings()
    if not get_all_settings():
        click.echo("Run trashcangourmand setsettings first")
        return None
    for settings in all_settings:
        # Cannot do this concurrently w/o difficulties
        set_curr_res(settings)
        message = get_message()
        send_message(message, datetime.date.today(), settings)
        click.echo("Message sent")
    click.echo("All messages sent.")

@cli.command()
def setcron():
    ### if no members of settings folder, error out
    if not get_all_settings():
        click.echo("Run trashcangourmand setsettings first")
        return None
    curr_cron = crontab.CronTab(user=True)
    if len(list(curr_cron.find_comment("trashcangourmandcron"))) > 0:
        click.echo("Trashcan Gourmand cron already set")
    else:
        job = curr_cron.new(command="trashcangourmand dish", comment="trashcangourmandcron")
        job.hour.on(5)
        curr_cron.write_to_user(user=True)
        click.echo("Trashcan Gourmand cron has now been set. Try running trashcangourmand dish to email you some stuff")

if __name__ == "__main__":
    cli()
