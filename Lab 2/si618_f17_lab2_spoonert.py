#!/usr/bin/python

'''
An old version was created by Dr. Yuhang Wang

'''
#coding: utf-8
import mrjob
from mrjob.job import MRJob
import re

WORD_RE = re.compile("\w+(?:'\w+|\w*)")

class BigramCount(MRJob):
  OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol
  
  def mapper(self, _, line):
    words = WORD_RE.findall(line)
    for w in range(len(words)-1):
        yield words[w].lower() + " " + words[w+1].lower(), 1

  def combiner(self, bigram, counts):
    yield bigram, sum(counts)
        
  def reducer(self, bigram, counts):
    yield bigram, str(sum(counts))

if __name__ == '__main__':
  BigramCount.run()