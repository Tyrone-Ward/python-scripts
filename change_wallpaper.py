#!/usr/bin/python

import urllib
import os
import sys
import subprocess
import json
import argparse

#TODO: Add controls (pause, newest, previous)
#TODO: Add more sources
#TODO: Create man page and auto completions
#DONE: Save images
#DONE: save and remeber wallpapers through boots


def set_image(image=None):
    subprocess.call(['hsetroot', '-cover', image])


def grab_image():
    k = json.loads(urllib.urlopen('https://api.desktoppr.co/1/wallpapers/random').read())
    pic_url = k['response']['image']['url']
    pic = urllib.urlretrieve(pic_url, os.path.join(os.environ['HOME'], 'Pictures', pic_url.split('/')[-1]))[0]
    return set_image(pic)


def restore():
    pic_dict = {}
    for pics in os.listdir(os.path.join(os.environ['HOME'], 'Pictures')):
        pic_dict.setdefault(os.path.join(os.environ['HOME'], 'Pictures', pics), os.stat(os.path.join(os.environ['HOME'], 'Pictures', pics)).st_ctime)
        sorted_pic_list = sorted(pic_dict, key=pic_dict.get, reverse=True)
        last_one = sorted_pic_list[0]
    return set_image(last_one)

parser = argparse.ArgumentParser(description='Wallpapers')
parser.add_argument('--restore', action='store_true', help='use last wallpaper')

args = parser.parse_args()

if args.restore:
    restore()
else:
    grab_image()
