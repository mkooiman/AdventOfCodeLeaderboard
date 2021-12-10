forked from 
https://github.com/tomswartz07/AdventOfCodeLeaderboard

#Whats different in this fork

This version checks for modifications of the list compared to the previous time it ran, it also gives a personalized congratulations message upon finishing any star. This is achieved by storing the last modification timestamp in a file called 'previous' 


[![Pylint](https://github.com/tomswartz07/AdventOfCodeLeaderboard/actions/workflows/pylint.yml/badge.svg)](https://github.com/tomswartz07/AdventOfCodeLeaderboard/actions/workflows/pylint.yml)

# Advent of Code Leaderboard Slack Bot

This repository contains the code for a script that will post a Private Advent of Code Leaderboard to a custom Slack Channel.

Useful for your friendly competitions in and around the workplace.

**What It Does:** Post the contents of a Private Advent of Code Leaderboard to your Slack Channel

**What It Does Not:** Fulfill your hopes and dreams (unless your hopes and dreams were to post the contents of a Private Advent of Code Leaderboard to your Slack Channel)

## Setup
**Prerequisites**:
- Python 3
- Working Internet Connection
- Admin Access to a Slack Team or the ability to bribe someone who does (I hear Christmas Cookies are nice this time of year‥)

**Process**:

1. Create a new [Incoming Slack Webhook](https://my.slack.com/services/new/incoming-webhook/)
    - Read more about incoming webhooks [here](https://api.slack.com/incoming-webhooks)
    - Feel free to customize it as you wish.
    - If you don't have access to add an incoming webhook, see the [Recommended Settings](#recommended-settings) section for more details.
2. Log in to Advent of Code and obtain two things: the Private Leaderboard ID Number and a Session Cookie.
See [Session Cookie](#getting-a-session-cookie) section for details.
3. Dump that info into a `secrets.py` file.
  - Webhook URL goes in the `SLACK_WEBHOOK` variable
  - Session goes in the `SESSION_ID` variable
  - Leaderboard ID goes in the `LEADERBOARD_ID` variable.
    - The ID is the last part of the leaderboard url (https://adventofcode.com/2018/leaderboard/private/view/LEADERBOARD_ID)
4. Run that shit. Schedule a cron job or something. I don't know. You're doing Advent of Code, figure it out. [Just make sure that you don't hit the servers too often.](https://www.reddit.com/r/adventofcode/comments/7gy2y3/remember_please_limit_automated_http_requests/)

## Docker Container
Since this script is fairly simple, it's easy enough to run in a compact docker
container, ensuring that the script is offloaded from whatever main host you have.

### Building Docker Image
There is a GitHub action which will build and deploy this container automatically,
but if you want to build it locally (i.e. to use a custom cron schedule)

1. Edit the `crontab` file to reflect the schedule you want. By default, it will
run at 7am daily during the month of the event. (Be sure to set the `TZ` env var
to your local time, otherwise UTC will be used)

2. Build the image
```
docker build -t slack-aoc .
```

3. Run the image
Refer to [Setup](#setup) to get the relevant parameters for your environment
```
docker run -it --detach --rm --name aoc-slack \
-e TZ="America/New_York" \
-e SLACK_WEBHOOK='https://hooks.slack.com/services/$HOOKINFO' \
-e LEADERBOARD_ID="$LEADERBOARD_ID" \
-e SESSION_ID="$SESSION_COOKIE" \
slack-aoc
```

## Recommended Settings
When creating the custom webhook for the Slack channel, there are a few options to customize.

It's also possible that you don't have access to add an incoming webhook to your team because of the permissions model. In that case, you would need to know what to send to the admin to get it set up. This is that stuff.

Here are the recommended settings when setting up the Hook:
- **Post to Channel:** Your `#adventofcode` channel, or `#general`
- **Descriptive Label:** Whatever you want. This isn't really necessary.
- **Customize Name:** "Advent of Code Leaderboard"
- **Customize Icon:** Pick an emoji → Christmas Tree

Copy the Webhook URL or have the Admin send that URL to you, you'll need it for the script.

## Getting a Session Cookie
You'll need a session cookie from the Advent of Code website.

Go to the [Advent of Code Private Leaderboard](https://adventofcode.com/2018/leaderboard/private) page. Make sure you're logged in.

### In Firefox:
- Open the Developer Tools by pressing `F12`
- Click on the small gear on the top right of the Developer Options pane
- Scroll down and make sure that "Storage" is checked under the Default Firefox Developer Options section
- Click on the Storage tab
- Open the Cookies section and copy the "Value" for "session"
- That value is what you put in place of `SESSION_COOKIE` in the script. (e.g. the line will read `COOKIES = {'session': 'THIS_IS_THE_SESSION_COOKIE'}`)

### In Chrome:
- Open the Developer Tools by pressing `CTRL` + `Shift` + `I`
    - Mac: Open the Developer Tools by pressing `Cmd` + `Opt` + `I`
- Select "Application" from the tool tabs
- Click the dropdown arrow beside cookies in treeview on the left
- Select *https://adventofcode.com*
- Double click the value of the *session* cookie to highlight it
- Right click and copy the value
- That value is what you put in place of `SESSION_COOKIE` in the script. (e.g. the line will read `COOKIES = {'session': 'THIS_IS_THE_SESSION_COOKIE'}`)
