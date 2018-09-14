# -*- coding:utf-8 -*-

import os
import urllib.parse
import urllib.request
import json
import random

def get_word():
    word_list = ['筋トレ','マッチョ','細マッチョ','肉体美']
    num = random.randrange(len(word_list))
    return word_list[num]


def get_image(word):
    img = []
    query_img = "https://www.googleapis.com/customsearch/v1?key=" + os.environ['GOOGLE_API_KEY'] + "&cx=" + os.environ['CUSTOM_SEARCH_ENGINE'] + "&q=" + urllib.parse.quote(word) + "&searchType=image"

    res = urllib.request.urlopen(query_img)
    data = json.loads(res.read().decode('utf-8'))
    num = random.randrange(len(data["items"]))
    img.append(data["items"][num]["image"]["thumbnailLink"])
    img.append(data["items"][num]["link"])

    return img

def send_line(message,image):
    LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + os.environ['LINE_NOTIFY_TOKEN']
    }
    body = {
        'message': message,
        'imageThumbnail':image[0],
        'imageFullsize':image[1],
    }
    data = urllib.parse.urlencode(body)

    req = urllib.request.Request(LINE_NOTIFY_URL, data=data.encode('utf-8'), method='POST', headers=headers)
    with urllib.request.urlopen(req) as res:
        response_body = res.read().decode("utf-8")

def lambda_handler(request, context):
    word = get_word()
    image = get_image(word)
    message = '筋トレしませんか？'
    send_line(message,image)
