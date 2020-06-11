import requests
# from requests.exception import RequestException
import os
from contextlib import closing
from bs4 import BeautifulSoup

# Twilio pword - Prosp3ct601!Prosp3ct601!
# groupme bot key - PqoB5KyzEU5BXSFmljTO7jxT4dvuWkjZmpNMYvHh
# groupme bot id - fa4d9cc813bdbd0f7d192054d4
# idea - why not just make it a groupme bot so i don't have to do sms stuff
# idea on idea - then i can make a group of bots to update me on the happenings of things!!!
# ^ that could also be handled by one main bot who has permissions to give updates about various things

def main():
    url = "https://www.georgerrmartin.com/notablog/"
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    grrmPost = html.find('div', class_='post').text.lower().split()

    command = "-1"
    message = ""

    for word in grrmPost:
        if (word == 'mexico' or word == 'winter'):
            message = "Possible Winds Update @ https://georgerrmartin.com/notablog/"
            command = "curl -d \'{\"text\" : \"" + message + "\", \"bot_id\" : \"fa4d9cc813bdbd0f7d192054d4\"}\' https://api.groupme.com/v3/bots/post"

    if(command != "-1"):
        os.system(command)

    return


main()
