# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 15:08:01 2017

@author: spoonertaylor
"""

import json
import gzip

# Load the compressed json file
data = list()
with gzip.open("yelp_academic_dataset.json.gz", "rb") as f:
    for line in f:
        json_str = line.decode('utf-8')
        json_data = json.loads(json_str)
        # Check if the lines is a business
        dat_type = json_data.get("type")
        if dat_type == "business":
            # Make list of jsons
            data.append(json.loads(json_str))

# get the needed data from each json block
def get_data(line):
    name = line.get('name')
    if name is None:
        name = "NA"
    city = line.get('city')
    if city is None:
        city = "NA"
    state = line.get('state')
    if state is None:
        state = "NA"
    stars = line.get('stars')
    if stars is None:
        stars = "NA"
    reviews = line.get('review_count')
    if reviews is None:
        reviews = "NA"
    main = line.get('categories')
    if main is None:
        main = "NA"
    elif len(main) == 0:
        main = "NA"
    else:
        main = main[0]
    return [name,city,state,str(stars),str(reviews),main]

# list of lists of data
dat = [get_data(l) for l in data]
# Write data to a tsv file.
with open('businessdata.tsv', 'w') as file:
    file.writelines('name\tcity\tstate\tstars\treview_count\tmain_category\n')
    file.writelines('\t'.join(i) + '\n' for i in dat)