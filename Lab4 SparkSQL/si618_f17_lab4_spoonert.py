# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 14:38:27 2017

Lab 4

Taylor Spooner
spoonert
"""
# Spark SQL
from pyspark import SparkContext
sc = SparkContext(appName="Lab4")

from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# Load data and register as a table
nfl_df = sqlContext.read.json("hdfs:///var/si618f17/NFLPlaybyPlay2015.json")
nfl_df.registerTempTable("nfl")

# Mean delta yards
# For each team sum the difference in their game yards less their oppenents.
# Then sum up yards across all games and take the mean.
q1 = sqlContext.sql("""	select tm1, sum(delta_yards) / count(*) as mean_delta_yards from (
	select  distinct G1, tm1, tm2, y1 - y2 as delta_yards from (
		select GameID as G1, posteam as tm1, sum(YardsGained) as y1 from nfl 
			group by GameID, posteam) t1
		inner join (
			select GameID as G2, posteam as tm2, sum(YardsGained) as y2 from nfl
			group by GameID, posteam) t2
		on t1.G1 = t2.G2
		where t1.tm1 <> t2.tm2) a
	group by tm1
	order by mean_delta_yards DESC""")

q1.collect()
q1.rdd.map(lambda i: '\t'.join(str(j) for j in i)) \
          .saveAsTextFile('delta yards')

#Play Ratio
# Find the ratio to runs to passes for each team.
q2 = sqlContext.sql("""select p1, runs / passes as run_pass_ratio from (
	select posteam as p1, count(*) as passes from nfl where PlayType = "Pass" group by posteam) r
	inner join (
		select posteam as p2, count(*) as runs from nfl where PlayType = "Run" group by posteam) p
	on p.p2 = r.p1
	order by run_pass_ratio""")
    
q2.collect()
q2.rdd.map(lambda i: '\t'.join(str(j) for j in i)) \
          .saveAsTextFile('run pass')

# Penalized
# Find the top 10 players in terms of number of penalties.
q3 = sqlContext.sql("""select PenalizedPlayer, PenalizedTeam, count(*) as num_pen from nfl
	where PenalizedPlayer is not null
	group by PenalizedPlayer, PenalizedTeam
	order by num_pen DESC, PenalizedTeam
	limit 10""")
q3.rdd.map(lambda i: '\t'.join(str(j) for j in i)) \
          .saveAsTextFile('penalized')


    


