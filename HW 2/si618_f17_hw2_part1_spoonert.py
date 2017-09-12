# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:22:14 2017

PART 1

@author: Taylor Spooner
unique name: spoonert
"""

from mrjob.job import MRJob
import re

WORD_RE = re.compile("[a-zA-Z0-9']+")

class MRMostUsedWord(MRJob):
    def mapper(self, _, line):
        words = WORD_RE.findall(line)
        for w in words:
            yield w.lower(), 1

    def combiner(self, word, counts):
        yield word, sum(counts)
    
    def reducer(self, word, counts):
        yield word, sum(counts)
        
        
if __name__ == "__main__":
   MRMostUsedWord.run()
