# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:23:57 2017
HW 1 Part 1
@author: spoonertaylor
"""
import json
import sqlite3
import os

os.chdir(r'C:\Users\Taylor\Documents\UMich\SI_618\HW 1')
# Read in the file
with open(r'.\movie_actors_data.txt', 'r') as file:
    data = file.readlines()
# Load as JSON
data_json = [json.loads(x) for x in data]
# Create SQLite database and tables
conn = sqlite3.connect('.\hw1database.db')
c = conn.cursor()

##### movie_genre table
# The movie genre movie will have two columns, the imdb_id and the genres
c.execute('CREATE TABLE movie_genre (imdb_id text, genre text);')

# Get the data from the JSON list
m_genre = list(zip([imdb.get('imdb_id') for imdb in data_json], \
            [g.get('genres') for g in data_json]))
# Some of the movies have more than one genre, so we are going to 
# have to seperate them.
m_genre2 = []
# Iterate over each tuple
for i, tup in enumerate(m_genre):
    # No movie genre, do not add data list
    if tup[1] is None:
        continue
    # Go over each genre and create new tuple
    else:
        for j, g in enumerate(tup[1]):
            m_genre2.append((tup[0], g))
            
c.executemany('INSERT INTO movie_genre VALUES (?, ?);', m_genre2)
conn.commit()

#### movies table
# movies table will have four columns: imdb_id, title, year, rating
# Create movie table
c.execute('CREATE TABLE movies (imdb_id text, title text, year real, rating real);')

mvs = list(zip([imdb.get('imdb_id') for imdb in data_json], \
                [title.get('title') for title in data_json], \
                 [yr.get('year') for yr in data_json], \
                  [rt.get('rating') for rt in data_json]))

c.executemany('INSERT INTO movies VALUES (?, ?, ?, ?);', mvs)
conn.commit()

#### movie_actor table
# The movie_actor table will have two columns, imdb_id and actors
c.execute('CREATE TABLE movie_actor (imdb_id text, actor text);')
# Get the data for the table
m_act = list(zip([imdb.get('imdb_id') for imdb in data_json], \
            [act.get('actors') for act in data_json]))

# Movies will have more than one actor,
# need to create a tuple for eaceh one
m_act2 = []
# Iterate over each original tuple
for i, tup in enumerate(m_act):
    # No actors, do not add data list
    if tup[1] is None:
        continue
    # Go over each actor and create new tuple
    else:
        for j, act in enumerate(tup[1]):
            m_act2.append((tup[0], act))

# Add data to table
c.executemany('INSERT INTO movie_actor VALUES (?, ?);', m_act2)
conn.commit()

####### 5)
# Find the top 10 genres with most movies and print results
top_genres = c.execute("""SELECT genre, count(*) as Count FROM movie_genre 
              GROUP BY genre ORDER BY Count DESC
              LIMIT 10;""")
print("Top 10 genres:")
print("Genre, Movies")
for i, tup in enumerate(top_genres.fetchall()):
    print(tup[0] + ", " + str(tup[1]))
print('\n')

###### 6)
# Find number of movies broken down by year in chronological order
mv_yr = c.execute("""SELECT year, count(*) as cnt FROM movies
                  GROUP BY year ORDER BY year;""")
print("Movies broken down by year:")
print("Year, Movies")
for i, tup in enumerate(mv_yr.fetchall()):
    print(str(int(tup[0])) + ", " + str(tup[1]))
print('\n')
##### 7) 
# Find all Sci-Fi movies order by decreasing rating, 
# then by decreasing year if ratings are the same
sci_fi = c.execute("""select title, year, rating from movies m
                   join movie_genre g on (m.imdb_id = g.imdb_id)
                   where g.genre == "Sci-Fi"
                   order by rating DESC, year DESC;""")
print("Sci-Fi Movies:")
print("Title, Year, Rating")
for i, tup in enumerate(sci_fi.fetchall()):
    print(tup[0] + ", " + str(int(tup[1])) + ", " + str(tup[2]))
print('\n')

####### 8)
# Find the top 10 actors who played in most movies in and after year 2000.
# Sort sby actor name
acts = c.execute("""select actor, count(*) as cnt from movie_actor a
                     left join movies m on m.imdb_id = a.imdb_id
                     where m.year >= 2000
                     group by a.actor
                     order by cnt DESC, actor
                     limit 10;""")
print("In and after year 2000, top 10 actors who played in most movies:")
print("Actor, Movies")
for i, tup in enumerate(acts.fetchall()):
    print(tup[0] + ", " + str(tup[1]))
print('\n')

##### 9)
# Find pairs of actors who co-stared in 3 or more movies. 
# The pairs of names must be unique.
pairs = c.execute("""select distinct case when act_a < act_b then act_a else act_b end as act_a,
	case when act_a < act_b then act_b else act_a end as act_b,
	cnt from (
		select act_a, act_b, count(*) as cnt from (
			select imdb_id, actor as act_a from movie_actor) a
			left join (select imdb_id, actor as act_b from movie_actor) b
			on a.imdb_id = b.imdb_id
			where act_a <> act_b
			group by 1,2) tb1
where cnt >= 3
order by cnt desc, act_a, act_b""")

print("Pairs of actors who co-stared in 3 or more movies:")
print("Actor A, Actor B, Co-stared Movies")
for i, tup in enumerate(pairs.fetchall()):
    print(tup[0] + ", " + tup[1] + ", " + str(tup[2]))
print('\n')                  

conn.close()
