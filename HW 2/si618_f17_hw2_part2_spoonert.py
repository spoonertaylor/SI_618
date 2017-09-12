# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:44:10 2017

PART 2

@author: Taylor Spooner
unique name: spoonert
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile("[a-zA-Z0-9']+")

class MRMostUsedWord(MRJob):
    # Write a mapper that seperates each word (lowercased) in a line
    def mapper_get_words(self, _, line):
        words = WORD_RE.findall(line)
        for w in words:
            yield w.lower(), 1

    # Combine the words by summing their counts
    def combiner_count_words(self, word, counts):
        yield word, sum(counts)
    
    # Sum all the counts up now
    # Yield a tuple (None, (count, word))
    def reducer_count_words(self, word, counts):
        yield None, (sum(counts), word)
    
    # Find the most frequent word by taking the max of the counts
    # The key for each is "None" which we ignore.
    def reducer_find_max_word(self, _, word_count_pairs):
        yield max(word_count_pairs)
    
    # Define our own steps so we can do a 2-Step MRJob
    # The reducer_count_words is the end of the first step,
    # Output of that is sent to the next step, which only has that one
    # reducer.
    def steps(self):
        return [
                MRStep(mapper = self.mapper_get_words,
                       combiner = self.combiner_count_words,
                       reducer = self.reducer_count_words),
                MRStep(reducer = self.reducer_find_max_word)
                ]
        
        
if __name__ == "__main__":
   MRMostUsedWord.run()
