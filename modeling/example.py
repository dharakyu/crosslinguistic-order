"""
Example script to illustrate use of ContinuousIncrementalRSA class
to compute utterance probabilities
"""

import numpy as np
import matplotlib.pyplot as plt

import string

from models import ContinuousIncrementalRSA
from utils import *

adjectives = ["red", "blue"]
nouns = ["pin", "dress", "truck"]
objects = get_all_objects(adjectives, nouns)
utterances = get_all_utterances(adjectives, nouns)
v_adj = 0.95
v_noun = 0.99
alpha = 5

rsa = ContinuousIncrementalRSA(adjectives=adjectives,
                                  nouns=nouns,
                                  objects=objects,
                                  utterances=utterances,
                                  v_adj=v_adj,
                                  v_noun=v_noun,
                                  alpha=alpha)

p_red = rsa.incremental_pragmatic_speaker({'color':'red', 'shape':'dress', 'string':'red dress'}, 'red')
print(p_red)
p_red_dress = rsa.incremental_pragmatic_speaker({'color':'red', 'shape':'dress', 'string':'red dress'}, 'red dress')
print(p_red_dress)