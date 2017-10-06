#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 23:57:23 2017

Get all of the facebook comments from the Ny Times facebook page.

@author: Ruixin Jiang, Taylor Spooner
"""

import urllib3
import json
import re
import emoji
import pandas as pd



access_token = ##YOUR ACCESS CODE

page_id = "nytimes"

# construct the URL string
base = "https://graph.facebook.com/v2.10"
node = "/" + page_id + "/posts"
parameters = "/?fields=created_time,id&since=2017-09-20&until=2017-09-27&access_token=%s" % access_token
url = base + node + parameters
# Get the first url
http = urllib3.PoolManager()
r = http.request('GET', url)
# Load it is json
data = json.loads(r.data)

# Loop through the rest of the links.
# Saving each post to a list.
has_next_page = True
posts_in_date = []
posts_in_date.append(data)
while(has_next_page):
    if 'paging' in data.keys():
        try:
            r = http.request('GET', data['paging']['next'])
            data = json.loads(r.data)
            posts_in_date.append(data)
        except:
            has_next_page = False
    else:
        has_next_page = False
post_id = []
for post in posts_in_date:
    for j in post['data']:
       post_id.append(j['id'])

# Now time to start to look at the comments.
parameters_c = "/?filter=stream&fields=id,message&access_token=%s" % access_token
comments = []
for i in post_id:
    next_page_c = True
    node_c = "/" + i + "/comments"
    url_c = base + node_c + parameters_c
    u = http.request('GET', url_c)
    com = json.loads(u.data)
    comments.append([i, com['data']])
    while(next_page_c):
        if 'paging' in com.keys():
            try:
                r1 = http.request('GET', com['paging']['next'])
                com = json.loads(r1.data)
                comments.append([i, com['data']])
            except KeyError:
                next_page_c = False
        else:
            next_page_c = False

# To get rid of all the emojis
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F650"  # emoticons
        u"\U0001F300-\U0001F5E3"  # symbols & pictographs
        u"\U0001F680-\U0001F6F8"  # transport & map symbols
        u"\U0001F1E0-\U0001F3FF"  # flags & Sports (iOS)
        u"\U0001F910-\U0001F9E6"  # Supplemental Symbols and Pictographs
        u'\u203C-\u2B50\u203C-\u2760]+'  # Miscellaneous Symbols
                           , flags=re.UNICODE)

d = []
s = '' # for emoji testing
for item in comments:
    for c in item[1]:
        m = emoji_pattern.sub(r'', c['message'])
        if m:
            d.append([item[0], c['id'], c['message']])
            s += m
        else:
            continue

# Test if there is emojis in all the comments
def text_has_emoji(text):
    r = [False]
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            r.append(character)
    return(r)

res = text_has_emoji(s)


# Put all of the information together
comments_df = pd.DataFrame(d)
comments_df['pagename'] = "nytimes"
comments_df.columns = ['post_id', 'comment_id', 'comment', 'pagename']

rand_100 = comments_df.sample(100)
rand_100 = rand_100[['pagename', 'post_id', 'comment_id', 'comment']]
rand_100.to_csv('si618_f17_lab5_random_sample_100_comments_rxjiang_spoonert.csv', index=False)
