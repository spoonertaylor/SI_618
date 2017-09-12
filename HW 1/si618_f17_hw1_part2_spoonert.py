# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:04:28 2017

HW 1 Part 2

@author: Taylor Spooner
unique name: spoonert
"""
import sys
import os
import json
import sqlite3

os.chdir(r'C:\Users\Taylor\Documents\UMich\SI_618\HW 1')

# First check the command line arguments
if len(sys.argv) != 3:
    print("Not enough arguments given. Aborting")
    sys.exit()
# Read in the two command line arguments
genre = sys.argv[1]
genre_low = genre.lower()
try:
    k = int(sys.argv[2])
except ValueError as ve:
    print("Please input an integer for the number of actors, k. Aborting")
    sys.exit()

# Read in the file
with open(r'.\movie_actors_data.txt', 'r') as file:
    data = file.readlines()
# Load as JSON
data_json = [json.loads(x) for x in data]
# Connect to SQL database that was already created.
conn = sqlite3.connect('.\hw1database.db')
c = conn.cursor()
# Query data table
acts = c.execute("""select actor, count(*) as cnt from movie_genre g
                     left join movie_actor a on g.imdb_id = a.imdb_id
                     where lower(g.genre) == '%s'
                     group by a.actor
                     order by cnt DESC, actor
                     limit %d;""" % (genre_low, k))
# Print results
print("Top %d actors who played in most %s movies:" % (k, genre))
print("Actor, %s Movies Played in" % genre)
for i, tup in enumerate(acts.fetchall()):
    print(tup[0] + ", " + str(tup[1]))
print('\n')

conn.close()
