#!/usr/bin/env python3.7
import datetime
import crontab
import click

@click.group()
def cli():
    pass

@cli.command()
def setsettings():
    ########
    ########
    ########
    pass

@cli.command()
def dish():
    ########
    ########
    ########
    pass

@cli.command()
def setcron():
    ### if no settings folder then error out
    #######
    #######
    #######
    #######
    curr_cron = crontab.CronTab(user=True)
    if len(list(curr_cron.find_comment("trashgourmandcron"))) > 0:
        pass # do nothing
    else:
        job = curr_cron.new(command="trashgourmand dish", comment="trashgourmandcron")
        job.hour.on(15)
        curr_cron.write_to_user(user=True)

if __name__ == "__main__":
    ######
    ######
    ######
    ######
    settings = some shit
    set_curr_img(settings)
    send_message(datetime.datetime.today(), settings)
