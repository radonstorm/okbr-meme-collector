import praw
import os
import requests
from datetime import datetime
import youtube_dl
from slugify import slugify

# create folders for saving posts
image_directory = os.path.join(os.path.dirname(__file__), 'images')
if not os.path.exists(image_directory):
    os.makedirs(image_directory)
image_directory = os.path.join(image_directory, str(datetime.now().date()))
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

# load client_id and secret from praw.ini
reddit = praw.Reddit(
    site_name='okbrbot',
    user_agent='python:com.radonstorm.okbrepicmemecollector:v0.1 (by u/neongamer100)'
)

# loop through top 25 posts
for post in reddit.subreddit('okbuddyretard').top('day', limit=25):
    filename = slugify(post.title)
    if filename == '':
        filename = slugify(post.id)
    # handle image posts
    if 'i.redd.it' in post.url:
        img = requests.get(post.url).content
        extension = post.url.split('.')[-1]
        with open(os.path.join(image_directory, f'{filename}.{extension}'), 'wb') as file:
            file.write(img)
    # handle video posts
    elif 'v.redd.it' in post.url:
        ytdl_opts = {
            'outtmpl': image_directory + f'/{filename}.%(ext)s',
            'quiet': True
        }
        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
            ytdl.download([post.url])
