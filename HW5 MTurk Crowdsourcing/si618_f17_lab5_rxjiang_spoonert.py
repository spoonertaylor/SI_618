# -*- coding: utf-8 -*-
"""
Use the FACEBOOK API to get all comments from New York Times posts 
between the dates 9/20/2017 to 9/26/2017.

This data is saved to a csv file to use for Amazon's MTurk Crowdsourcing site.

Authors: Taylor Spooner, Ruixin Jiang
"""

import urllib3
import json
import datetime
import random
import time
import re
import pandas as pd

access_token = ## PUT IN YOUR OWN ACCESS CODE.

page_id = "nytimes"

# construct the URL string
base = "https://graph.facebook.com/v2.4"
node = "/" + page_id + "/feed"
parameters = "/?fields=id,created_time,comments&filter=stream&access_token=%s" % access_token
url = base + node + parameters
# Get URL
http = urllib3.PoolManager()
r = http.request('GET', url)
# Load data as json
data = json.loads(r.data)
# Go through each page of the NY Times
has_next_page = True
posts_in_date = []
while(has_next_page):
    # If page was not loaded correctly, break from loop
    if 'error' in data.keys():
        e = data.get('error')
        code = e.get('code')
        message = e.get('message')
        print(code)
        print(message)
        break
    dat = data.get('data')
    try:
        # Go through each post on page
        for post in dat:
            # Check if between 9/20/2017 - 9/26/2017
            date = post.get('created_time')
            date = datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%S+0000')
            date = date.strftime('%Y-%m-%d')
            if '2017-09-20' <= date and date <= '2017-09-26':
                posts_in_date.append(post)
            # Once we have found posts earlier than our end date we can stop
            if date < '2017-09-20':
                has_next_page = False
    except TypeError:
        break
    # Go to next page
    if 'paging' in data.keys():
        try:
            r = http.request('GET', data['paging']['next'])
            data = json.loads(r.data)
        except KeyError:
            has_next_page = False
    else:
        has_next_page = False
        
# So now we have all the posts within the date range.

### can't get rid of 
# '✨❤️❤️✨' 
# hearts are 
# Sparkles are u"\U000FEB60"
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

# Now time to start to look at the comments.
comments = []
post_id = []
comment_id = []
for p in posts_in_date:
    # Flags as we crawl through comments
    has_next_page = True
    first = True
    # As long as there is a next page
    while(has_next_page):
            # If page was not loaded correctly, break from loop
        if 'error' in data.keys():
            e = data.get('error')
            code = e.get('code')
            message = e.get('message')
            print(code)
            print(message)
            break
        # Check to see if we are on the first iteration
        if first:
            dat = p.get('comments')
            # Just for the very first time, get the post id.
            p_id = p.get('id')
        else:
            dat = data
        # Get the comments data
        coms = dat.get('data')
        # Go through each comment in that post on that page.     
        for c in coms:
            message = c.get('message')
            # Get the comment id for each comment
            c_id = c.get('id')
            # Clean message of emojis
            message = emoji_pattern.sub(r'', message)
            # Make sure we still have a comment left.
            if len(message) > 0:
                comments.append(message)
                comment_id.append(c_id)
                # Make a list of equal size, adding the post id for each comment.
                post_id.append(p_id)

        # Check if there is another page.
        if 'paging' in dat.keys():
            # Try to go to next page
            try:
                r = http.request('GET', dat['paging']['next'])
                data = json.loads(r.data)
                first = False
            except KeyError:
                has_next_page = False
        else:
            has_next_page = False

n_comments = len(comments)

# Put all of the information together
comments_df = pd.DataFrame (
        {'pagename' : "nytimes",
        'post_id' : post_id,
        'comment_id' : comment_id,
        'comment' : comments}
        )

rand_100 = comments_df.sample(100)
rand_100 = rand_100[['pagename', 'post_id', 'comment_id', 'comment']]
rand_100.to_csv('si618_f17_lab5_random_sample_100_comments_rxjiang_spoonert.csv', index=False)