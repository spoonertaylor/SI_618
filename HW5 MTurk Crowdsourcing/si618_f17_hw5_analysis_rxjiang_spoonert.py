# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 17:09:44 2017

@author: spoonertaylor
"""

import pandas as pd

data = pd.read_csv("si618_f17_hw5_cleaned_data_rxjiang_spoonert.csv", encoding="latin-1")

# Agreement
def all_agree(line):
    answers = line[3:9]
    num_nonzero = answers.iloc[answers.nonzero()[0]]
    if len(num_nonzero) == 1:
        return True
    else:
        return False

data['agree'] = data.apply(lambda row: all_agree(row), axis=1)
prop_agree = data['agree'].mean()


# At least two
def at_least_2(line):
    answers = line[3:9]
    num_nonzero = answers.iloc[answers.nonzero()[0]]
    if len(num_nonzero) <= 2:
        return True
    else:
        return False

data['agree_2'] = data.apply(lambda row: at_least_2(row), axis=1)
prop_atleast2 = data['agree_2'].mean()

# Personal attacks
def personal_attack(line):
    pers_att = line[3]
    if pers_att > 0:
        return True
    else:
        return False

data['personal_attack'] = data.apply(lambda row: personal_attack(row), axis=1)
prop_persatt = data['personal_attack'].mean()