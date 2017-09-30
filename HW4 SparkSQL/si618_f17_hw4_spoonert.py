# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:19:24 2017

HW 4 
Taylor Spooner
spoonert
"""
# Spark SQL
import csv

from pyspark import SparkContext
sc = SparkContext(appName="HW4")

from pyspark.sql import SQLContext
from pyspark.sql.functions import *
sqlContext = SQLContext(sc)

# Load data and register as a table
yelp_bus = sqlContext.read.json("hdfs:///var/si618f17/yelp_academic_dataset_business.json")
yelp_bus.registerTempTable("bus")

yelp_rev = sqlContext.read.json("hdfs:///var/si618f17/yelp_academic_dataset_review.json")
yelp_rev.registerTempTable("revs")

# Question 1
# Count the number of cities each reviewer reviews in
# Then count reviewers in each number of cities.
q1 = sqlContext.sql("""select cities, count(*) as yelp_users from (
	select user_id, count(*) as cities from (
		select distinct user_id, city from (
			select * from bus
				inner join revs
				on bus.business_id = revs.business_id) t1) t2
	group by user_id) t3
group by cities
order by cities""")

#q1 = q1.select(col("cities").alias("cities"), col("yelp_users").alias("yelp users"))
#q1.save('si617_f17_hw4_output_allreview_spoonert.csv', 'com.databricks.spark.csv').option("header", "true")
q1.collect()
q1.rdd.map(lambda i: ','.join(str(j) for j in i))
#q1.write.csv('si618_f17_hw4_output_allreview_spoonert.csv', header=True)

with open('si618_f17_hw4_output_allreview_spoonert.csv', 'wb') as csvfile:
    all_rev = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    all_rev.writerow(["cities", "yelp users"])
    for row in q1.collect():
        all_rev.writerow(row)

## Question 2
## Do the same analysis but filter into good and bad reviews
## good reviews, stars for a review > 3
good = sqlContext.sql("""select cities, count(*) as yelp_users from (
	select user_id, count(*) as cities from (
		select distinct user_id, city from (
			select * from bus
				inner join revs
				on bus.business_id = revs.business_id
			where revs.stars > 3) t1) t2
	group by user_id) t3
group by cities
order by cities""")

good.collect()
good.rdd.map(lambda i: ','.join(str(j) for j in i))
with open('si618_f17_hw4_output_goodreview_spoonert.csv', 'wb') as csvfile:
    good_rev = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    good_rev.writerow(["cities", "yelp users"])
    for row in good.collect():
        good_rev.writerow(row)    
    
   
# Bad reviews, stars for a review < 3
bad = sqlContext.sql("""select cities, count(*) as yelp_users from (
	select user_id, count(*) as cities from (
		select distinct user_id, city from (
			select * from bus
				inner join revs
				on bus.business_id = revs.business_id
			where revs.stars < 3) t1) t2
	group by user_id) t3
group by cities
order by cities""")
    
bad.collect()
bad.rdd.map(lambda i: ','.join(str(j) for j in i))
with open('si618_f17_hw4_output_badreview_spoonert.csv', 'wb') as csvfile:
    bad_rev = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    bad_rev.writerow(["cities", "yelp users"])
    for row in bad.collect():
        bad_rev.writerow(row) 