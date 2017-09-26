# -*- coding: utf-8 -*-
'''
HW 3
Taylor Spooner
Unique Name: spoonert

spark-submit --master yarn-client --queue si618f17 --num-executors 2 --executor-memory 1g   --executor-cores 2  si618_f17_hw3_spoonert.py
'''

import json
from pyspark import SparkContext

sc = SparkContext(appName="ReviewCount")

input_file = sc.textFile("hdfs:///var/si618f17/yelp_academic_dataset_business.json")

def city_star(data):
    cat_star_list = []
    stars = data.get('stars', None)
    city = data.get('city', None)
    neigh = data.get('neighborhoods', None)
    review_count = data.get('review_count', None)
    if neigh:
        for n in neigh:
            if stars != None and review_count != None:
                cat_star_list.append(((city,n), (1, review_count, stars)))
    else:
        cat_star_list.append(((city,"Unknown"), (1, review_count, stars)))
    return cat_star_list

def star_four(line):
    stars = line[2]
    if stars >= 4:
        return (line[0], line[1], 1)
    else:
        return (line[0], line[1], 0)

city_stars = input_file.map(lambda line: json.loads(line)) \
                           .flatMap(city_star) \
                           .mapValues(star_four) \
                           .reduceByKey(lambda x,y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]))
            
city_stars_sorted = city_stars.sortBy(lambda x: (x[0][0], -x[1][0], -x[1][1], -x[1][2], x[0][1]))
city_stars_sorted_map = city_stars_sorted.map(lambda t: t[0][0] + '\t' + t[0][1] + '\t' + str(t[1][0]) + '\t' + str(t[1][1]) + '\t' + str(t[1][2]))
                                         
city_stars_sorted_map.saveAsTextFile("hdfs:///user/spoonert/si618_f17_hw3_output_spoonert")

# flatMap -- ("category", star_value)
# mapValues -- ("Category", (star_value, 1))
# reduce by key ("category", (sum(star), sum(number reviews)))
# map (no longer looks at the Key) -- ("category", avg_stars)
