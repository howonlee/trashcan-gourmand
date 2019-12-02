#!/usr/bin/env python3.7
import os
import time
import crontab
import click
from typing import Union, List
from settings import Settings
import emailer

@click.group()
def cli():
    pass

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
    return list(map(Settings.from_file, settings_filenames))

def process_filetypes(filetypes: str) -> Union[str, List[str]]:
    if "," not in filetypes:
        return filetypes
    else:
        return list(map(lambda x: x.strip(), filetypes.split(",")))


@cli.command()
def setsettings():
    settings_path = get_settings_path()
    root_dir = input("Root dir (the root dir of the project to email >")
    filetypes = process_filetypes(input("Filetypes (the filetypes to email): separated by commas. For example, .py,.js >"))
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
    click.echo("New settings saved. Now go run trashcangourmand setcron")

@cli.command()
def dish():
    all_settings = get_all_settings()
    if not get_all_settings():
        click.echo("Run trashgourmand setsettings first")
        return None
    for settings in all_settings:
        # Cannot do this concurrently w/o difficulties
        emailer.set_curr_res(settings)
        message = emailer.get_message()
        emailer.send_message(message, datetime.datetime.today(), settings)
        click.echo("Message sent")
    click.echo("All messages sent.")

@cli.command()
def setcron():
    ### if no members of settings folder, error out
    if not get_all_settings():
        click.echo("Run trashgourmand setsettings first")
        return None
    curr_cron = crontab.CronTab(user=True)
    if len(list(curr_cron.find_comment("trashgourmandcron"))) > 0:
        click.echo("Trashcan Gourmand cron already set")
    else:
        job = curr_cron.new(command="trashgourmand dish", comment="trashgourmandcron")
        job.hour.on(5)
        curr_cron.write_to_user(user=True)
        click.echo("Trashcan Gourmand cron has now been set. Try running trashcangourmand dish to email you some stuff")

if __name__ == "__main__":
    cli()
