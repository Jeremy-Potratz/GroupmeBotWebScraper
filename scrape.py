import requests
import os
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


holder = ""
counter = 0
sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=5)
def main():
    nintendo()
    grrm()
    return

# both of these are going to alert me every hour if something pops up unfortunately
# need to figure out a way to get dates maybe or the last title and see if it is different


def nintendo():
    #i know this is really similar to the grrm function but i believe the two will grow more different the more i develop
    global holder
    global counter
    url = "http://www.nintendolife.com/news"
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    nintendoLife = html.find_all('span', class_='title')

    for title in nintendoLife:
        words = title.text.lower()
        # gotta figure out how to get the most recent one that is new. rn i can get new ones, but also old ones 
        if(holder != words and counter == 0):
            if (words.find('pikmin') != -1 or words.find('breath of the wild') != -1):
                print(words)
                holder = words
                print(holder)
                message = "Possible nintendo Update @ " + url
                command = "curl -d \'{\"text\" : \"" + message + "\", \"bot_id\" : \"fa4d9cc813bdbd0f7d192054d4\"}\' https://api.groupme.com/v3/bots/post"
                # os.system(command)
                return
    return


def grrm():
    url = "https://www.georgerrmartin.com/notablog/"
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    grrmPost = html.find('div', class_='post').text.lower().split()

    for word in grrmPost:
        if (word == 'winds' or word == 'winter'):
            message = "Possible Winds Update @ " + url
            command = "curl -d \'{\"text\" : \"" + message + "\", \"bot_id\" : \"fa4d9cc813bdbd0f7d192054d4\"}\' https://api.groupme.com/v3/bots/post"
            os.system(command)
            return
    return


# main()


sched.start()
