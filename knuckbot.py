import requests
import oauth2 as oauth
import os
import urllib
import argparse
import json
from twitter import *
from random import randint
from PIL import Image, ImageDraw, ImageFont

# Constants
post_tweet_endpoint = 'https://api.twitter.com/1.1/statuses/update.json'
upload_photo_endpoint = 'https://upload.twitter.com/1.1/media/upload.json'

# Fetch environment variables
CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
ACCESS_KEY = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

# Create client
t = Twitter(
    auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

def get_knuck(word):
    img = Image.open('knuckles.jpg')

    fnt = ImageFont.truetype('./AnglicanText.ttf', 40)
    fill=(0,0,0)
    d = ImageDraw.Draw(img)

    d.text((58,120), word[0], font=fnt, fill=fill)
    d.text((92,120), word[1], font=fnt, fill=fill)
    d.text((124,116), word[2], font=fnt, fill=fill)
    d.text((156,117), word[3], font=fnt, fill=fill)

    d.text((188,115), word[5], font=fnt, fill=fill)
    d.text((219,113), word[6], font=fnt, fill=fill)
    d.text((252,112), word[7], font=fnt, fill=fill)
    d.text((278,114), word[8], font=fnt, fill=fill)

    return img


#First things first, we need to open up a file and read each one into a list
def openFile(filename):
    with open (filename) as f:
        return f.read().splitlines()

    # print(verbs, nouns, adjectives, adverbs)
def generateTat():
    #Open files
    words = openFile('fourLetterNouns.txt') + openFile('fourLetterAdverb.txt') + openFile('fourLetterVerbs.txt') + openFile('fourLetterAdjective.txt')
    #grab first words
    wordLength = len(words)-1
    #pick random number
    random = randint(0, wordLength)
    rand2 = randint(0, wordLength)

    word1 = words[random].lower()
    word2 = words[rand2].lower()
    return word1+ " " + word2


def upload_image(image, status):
    image.save("tat.jpg")
    with open("tat.jpg", "rb") as imagefile:
        imagedata = imagefile.read()

    # - then upload medias one by one on Twitter's dedicated server
    #   and collect each one's id:
    t_upload = Twitter(domain='upload.twitter.com',
        auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
    print("uploaded with id_img1: ", id_img1)
    print("status is: ", status)

    # - finally send your tweet with the list of media ids:
    t.statuses.update(status=status, media_ids=",".join([id_img1]))

def lambda_handler(_event_json, _context):
    words = generateTat()
    print("wrods", words)
    image = get_knuck(words)
    upload_image(image, words)
