import requests
import os
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
# idea - why not just make it a groupme bot so i don't have to do sms stuff
# idea on idea - then i can make a group of bots to update me on the happenings of things!!!
# ^ that could also be handled by one main bot who has permissions to give updates about various things

# in the future - i could centralize all my scraping to this one bot and change my message based off of that
#basically just return what i want to say based off of different websites and say it, then
#i can leave the scheduler on main and have everything searched at once
#news about an update - Hunter x Hunter, Pikmin 4, BOTW 2
#could connect to the spotify api to learn about new music i might like !!!
# could look into my email possibly, idk if thats good though


nintendoHolder = []
grrmHolder = ""
sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=1)
def main():
    nintendo()
    grrm()
    return

# both of these are going to alert me every hour if something pops up unfortunately
# need to figure out a way to get dates maybe or the last title and see if it is different


def nintendo():
    global nintendoHolder
    ninList = []
    url = "http://www.nintendolife.com/news"
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    nintendoLife = html.find_all('span', class_='title')

    for title in nintendoLife:
        words = title.text.lower()
        if (words.find('pikmin') != -1 or words.find('breath of the wild') != -1):
            ninList.append(words)
    # ninlist holds all titles that have the words in them
    # we put all the ones we have already consoled into the holderList
    ifs = 0
    for nin in ninList:
        for h in nintendoHolder:
            if nin == h:
                ifs = 1
        if (ifs != 1):
            message = datetime.now().strftime("%m/%d/%Y %H:%M:%S") + " Possible Nintendo Update @ " + url
            command = "curl -d \'{\"text\" : \"" + message + "\", \"bot_id\" : \"fa4d9cc813bdbd0f7d192054d4\"}\' https://api.groupme.com/v3/bots/post"
            nintendoHolder.append(nin)
            os.system(command)
        ifs = 0
    return


def grrm():
    global grrmHolder
    url = "https://www.georgerrmartin.com/notablog/"
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    grrmPost = html.find('div', class_='post').text.lower().split()

    if(grrmHolder != grrmPost):
        for word in grrmPost:
            if (word == 'winds' or word == 'winter'):
                grrmHolder = grrmPost
                message = datetime.now().strftime("%m/%d/%Y %H:%M:%S") + " Possible Winds Update @ " + url
                command = "curl -d \'{\"text\" : \"" + message + "\", \"bot_id\" : \"fa4d9cc813bdbd0f7d192054d4\"}\' https://api.groupme.com/v3/bots/post"
                os.system(command)
                return
    return


sched.start()
