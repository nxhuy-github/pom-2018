import sys, json, numpy as np
import pandas as pd

def weight_transaction(row):
     count = 0
     for r in row:
          if r == 1:
               count = count + 1
          else:
               pass
     return 2**count

def weights_transactions(array):
     weights = []
     for row in array:
          weight = weight_transaction(row)
          weights.append(weight)
          weight = 0
     return weights

def probabilities_transactions(weights):
     s = sum(weights)
     props = []
     for i in weights:
          p = i * 1.0 / s
          props.append(p)
     return props

def create_interval(weights):
     interval = [0]
     tmp = 0
     for x in weights:
          tmp = tmp + x
          interval.append(tmp)
     return interval

def draw(nrt, interval):
     resultat = 0
     for i, x in enumerate(interval):
          if (i + 1) is not None:
               if x <= nrt and nrt < interval[i + 1]:
                    resultat = i
                    break
          else:
               pass
     return resultat

def random_transaction(weights):
     nrt = np.random.uniform(0, sum(weights))
     interval = create_interval(weights)
     resultat = draw(nrt, interval)
     return resultat

def extract_motif(transaction):
     motif = []
     metrics = []
     items = {}
     for i, t in enumerate(transaction):
          if i != 0:
               items['i'+str(i)] = 0
               if t == 1:
                    if np.random.randint(0, 2) == 1:
                         motif.append('i'+str(i))
                         items['i'+str(i)] = 1
                         metrics.append(i)
     return motif, metrics, items




