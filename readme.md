> I already am eating from the trash can all the time. The name of this trash can is ideology.  The material force of ideology makes me not see what I am effectively eating.
> - S. Žižek

> S. Žižek is a raccoon who lived in a dumpster behind a university's library who was transformed into a human by a witch
> - B. Sutton

# Trashcan Gourmand

Trashcan Gourmand is a tool to help you remember the details of your programming projects. It does this by sending you a randomly chosen bit of source code from a project every day.

Every day it causes you to email yourself the image of an individual source file from a project which you choose. Because there is no hosting and it is all done on your machine, I don't have to janitor anything besides the mail and my machine, and you don't have to do anything except for your mail and your machine.

It has been my experience that my judgment of a source file's importance to a project has been terrible, so this tool chooses source files completely randomly, given a filetype or filetypes. This is eating from the trashcan of your project.

It only works on POSIX right now. This will probably stay that way for the foreseeable future.

# Getting Started

## Requirements

- Python 3.7
- I say POSIX OS but I'm only realistically going to test it on OSX and Ubuntu so those, or whatever you'd like to wrangle

Run `pip install -r requirements.txt` to install packages if you're developing.

## Installation

`pip install trashcangourmand`

## Usage

- `trashcangourmand setsettings` goes through an interactive thing to set settings so Trashcan Gourmand can get your machine to email itself.

You can set multiple settings by going through `setsettings` multiple times, one for each project you want to email. It will email one email per project (be careful about your email provider's email limits). It's your email which is sending, so don't email anyone you don't want to spam with the internal details of your projects.

`setsettings` creates settings files, which are just json files, in `~/.trashcangourmet`. Remove them if you want to not be emailed anymore.

- `trashcangourmand setcron` sets your crontab settings to do `trashcangourmand dish` every day at 5am system time. Sets crontab on current user, no interaction needed, but this won't work with anacron.

If you want to set up anacron on root, which I usually do, it looks something more like

```
sudo sh -c 'echo "#!/bin/bash -e
> sudo -H -u <your username> trashcangourmand dish" >> /home/<your username>/.trashcangourmand/trashcangourmand.log 2>&1'
```

And if you want run-parts in cron-daily to have them, the script to put in `cron.daily` looks more like

```
#!/bin/bash -e
sudo -H -u <your username> trashcangourmand dish" >> /home/<your username>/.trashcangourmand/trashcangourmand.log 2>&1
```

- `trashcangourmand dish` dishes out an image of an individual source file.

# Troubleshooting

## I have a laptop and it emails intermittently.

Depending on your crontab implementation, usually missed dates in cronjobs on a laptop will miss the cron runs in your laptop. Use an always-on box or spin up a cloud instance or something if you need it to always run. Use anacron if you just want it to run eventually, when the laptop is on.

## It doesn't email at all.

Check if you got the email _app_ password and that you have all the email configuration settings right. Your normal email password will have the 2FA or whatever on.

## The security (or lack thereof) terrifies me.

Reasonable. This is not really a serious project. Maybe don't use it for the ultra secret things?

# Contributing

I will respond to issues and emails if I feel like it, otherwise not. I have a job and stuff, full-time support isn't happening.

If you'd like to contribute, just email me (Howon) sometime before putting up a PR or something. I may or may not reply, depends upon how I feel like it.

# License

MIT.
