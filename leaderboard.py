#!/usr/bin/env python
'''
This script will grab the leaderboard from Advent of Code and post it to Slack
'''
# pylint: disable=wrong-import-order
# pylint: disable=C0301,C0103,C0209

import os
import datetime
import sys
import json
import requests

LEADERBOARD_ID = os.environ.get('LEADERBOARD_ID')
SESSION_ID = os.environ.get('SESSION_ID')
SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')

# If the ENV Var hasn't been set, then try to load from local config.
# Simply create secrets.py with these values defined.
# See README for more detailed directions on how to fill these variables.
if not all([LEADERBOARD_ID, SESSION_ID, SLACK_WEBHOOK]):
    from secrets import LEADERBOARD_ID, SESSION_ID, SLACK_WEBHOOK

# You should not need to change this URL
LEADERBOARD_URL = "https://adventofcode.com/{}/leaderboard/private/view/{}".format(
        datetime.datetime.today().year,
        LEADERBOARD_ID)

def formatCongratsMessage(members_json, timestamp):
    message = ""
#    print("formatCongrats")
    for member in members_json.values():
        memberMessage = ":star: Congratulations " + member["name"] + " on completing: "
        completed = False
        for day, stars in member["completion_day_level"].items():
            for starNr, star in stars.items():
#                print( member["name"] + " "+ str(day) + " " +  str(star["get_star_ts"] )+">"+str(timestamp))
                if star["get_star_ts"] > timestamp:
                    if completed:
                        memberMessage += ", "
                    memberMessage += "day " + str(day) + " star " + str(starNr)
                    completed = True
#                    print(memberMessage)
        if completed:
            message += memberMessage +"\n"
    return message

def formatLeaderMessage(members):
    """
    Format the message to conform to Slack's API
    """
    message = ""

    # add each member to message
    medals = [':third_place_medal:', ':second_place_medal:', ':trophy:']
    for username, score, stars, last in members:
        if medals:
            medal = ' ' + medals.pop()
        else:
            medal = ''
        message += f"{medal}*{username}* {score} Points, {stars} Stars\n"

    message += f"\n<{LEADERBOARD_URL}|View Leaderboard Online>"

    return message

def parseMembers(members_json):
    """
    Handle member lists from AoC leaderboard
    """
    # get member name, score and stars
    members = [(m["name"],
                m["local_score"],
                m["stars"],
                m["last_star_ts"]
                ) for m in members_json.values()]
    
    # sort members by score, descending
    members.sort(key=lambda s: (-s[1], -s[2]))

    return members


def postMessage(message):
    """
    Post the message to to Slack's API in the proper channel
    """
    payload = json.dumps({
        "icon_emoji": ":christmas_tree:",
        "username": "Advent Of Code Leaderboard",
        "text": message
    })

    requests.post(
        SLACK_WEBHOOK,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

def main():
    """
    Main program loop
    """
    # make sure all variables are filled
    if LEADERBOARD_ID == "" or SESSION_ID == "" or SLACK_WEBHOOK == "":
        print("Please update script variables before running script.\n\
                See README for details on how to do this.")
        sys.exit(1)

    # retrieve leaderboard
    r = requests.get(
        "{}.json".format(LEADERBOARD_URL),
        cookies={"session": SESSION_ID}
    )
    if r.status_code != requests.codes.ok: #pylint: disable=no-member
        print("Error retrieving leaderboard")
        sys.exit(1)

    # get members from json
    members = parseMembers(r.json()["members"])
      
    last_star = 0
    
    for username, score, stars, last in members:
        if last > last_star:
            last_star = last

    f  = open('previous', 'r')
    previous = f.read()
    f.close()
    if previous == str(last_star):
        sys.exit(1)
    f = open ('previous','w')
    f.write(str(last_star))
    f.close()
    
    starMessage = formatCongratsMessage(r.json()["members"], int(previous))

    # generate message to send to slack
    message = formatLeaderMessage(members)

    # send message to slack
    postMessage(starMessage + "\n" + message)

if __name__ == "__main__":
    main()
