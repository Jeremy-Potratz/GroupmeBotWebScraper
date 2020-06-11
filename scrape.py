import requests
import os
from contextlib import closing
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

# idea - why not just make it a groupme bot so i don't have to do sms stuff
# idea on idea - then i can make a group of bots to update me on the happenings of things!!!
# ^ that could also be handled by one main bot who has permissions to give updates about various things

# in the future - i could centralize all my scraping to this one bot and change my message based off of that
#basically just return what i want to say based off of different websites and say it, then
#i can leave the scheduler on main and have everything searched at once
#news about an update - Hunter x Hunter, Pikmin 4, BOTW 2
#could connect to the spotify api to learn about new music i might like !!!
# could look into my email possibly, idk if thats good though

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=1)
def main():
    url = "https://www.georgerrmartin.com/notablog/"
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    grrmPost = html.find('div', class_='post').text.lower().split()
    command = "-1"
    message = ""

    for word in grrmPost:
        if (word == 'winds' or word == 'winter'):
            message = "Possible Winds Update @ https://georgerrmartin.com/notablog/"
            command = "curl -d \'{\"text\" : \"" + message + "\", \"bot_id\" : \"fa4d9cc813bdbd0f7d192054d4\"}\' https://api.groupme.com/v3/bots/post"

    if(command != "-1"):
        os.system(command)
    return

sched.start()
