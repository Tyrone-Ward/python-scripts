#!/usr/bin/python

import urllib
import os
import threading
import Queue
import string 

import imgurpython
from imgurpython import ImgurClient

# TODO: add metrics downloaded x images in x {min or sec}

q = Queue.Queue(maxsize=0)
# Change the number of simultaneous threads
num_threads = 10

client_id = ''
client_secret = ''

client = ImgurClient(client_id, client_secret)
gallery_url = raw_input('Enter gallery URL: ').split('/')[-1]

try:
    gallery = client.gallery_item(gallery_url)
except(imgurpython.helpers.error.ImgurClientError):
    gallery = client.get_album(gallery_url)

download_path = os.path.join('c:', os.environ['HOMEPATH'], 'Downloads')

os.chdir(download_path)

if isinstance(gallery.title, unicode) is False:
    print 'has no title'
    gallery.title = gallery.id
else:
    gallery.title = str(gallery.title).translate(None, string.punctuation)


print(gallery.title)
os.mkdir(gallery.title)
os.chdir(gallery.title)

for x in gallery.images:
    q.put(x['link'])

def worker():
    while True:
        item = q.get()
        urllib.urlretrieve(item, item.split('/')[-1])
        print "{0} of {1} completed.".format(gallery.images_count - q.qsize(), q.qsize())
        q.task_done()

for i in range(num_threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

q.join()
