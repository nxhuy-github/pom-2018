import pandas as pd
import numpy as np
import scipy.stats
import os
from collections import OrderedDict
import copy

def read_csv(link):
     '''
     Read data from CSV file
     Paramaters
     ----------
     @link : string
          path to CSV file

     Returns
     ----------
     DataFrame:
          object contains data
     '''
     df = pd.read_csv(link)
     #return df.to_json(orient='records')
     return df

def cover_coverage_pos_neg(array, metrics):
     '''
     Create an array: 1 if the motif in the transaction, 0 if not
     Calculate coverage
     Calculate the positive coverage
     Calculate the negative coverage (pos_c + neg_c = coverage)

     Parameters
     ----------
     @array: list
          array contains data of the transactions
     @metrics: array
          array contains the number value of motif
     Returns
     ----------
     array:
          the value's element is either 1 or 0
     int:
          coverage, positive coverage, negative coverage
     '''
     cover = {}
     coverage = 0
     pos_c = 0
     for row in array:
          count = 0
          for i in metrics:
               if row[i] == 1:
                    count = count + 1
          if count == len(metrics):
               cover[row[0]] = 1
               coverage = coverage + 1
               if row[-1] == 1: # supposons que le derniere item est 'item/attribut target'
                    pos_c = pos_c + 1
          else:
               cover[row[0]] = 0
     neg_c = coverage - pos_c
     return cover, coverage, pos_c, neg_c

def chi_square(cover, weights):
     '''
     Calculate the chi square
     
     Parameters
     ----------
     @cover: array
          the cover of a motif
     @weights: array
          the weights of all transactions

     Return
     ----------
     float:
          the chi square
     '''
     w = []
     i = 0
     for (k, v) in cover.items():
          if v == 0:
               w.append(0)
          else:
               w.append(weights[i])
          i = i + 1
     obs = np.array([w, weights])
     resultat = scipy.stats.chisquare(obs, axis=None)[0]
     #resultat = scipy.stats.chi2_contingency(obs)[0]
     return resultat

def items_in_motif(motif, items):
     '''
     Find out which item in the motif

     Parameters
     ----------
     @motif: array
     @items: array
          the array of items

     Return
     ----------
     dictionary:
          key: item
          value: 1 if item in motif, 0 if not
     '''
     result = {}
     for i in items:
          if i != 'tid':
               if i in motif:
                    result[i] = 1
               else:
                    result[i] = 0
     return result

def store_data(data, filename):
     '''
     Save data in CSV file

     Parameters
     ----------
     @data: array
     @filname: string

     Return
     ----------
     void
     '''
     df = pd.DataFrame(data)
     if os.stat(filename).st_size == 0:
          column_name = sorted(list(data[0].keys()))
          #print('Column name: ',column_name)
          df.to_csv(filename, columns=column_name, encoding='utf-8', mode='a', index=False)
     else:
          df.to_csv(filename, header=False, encoding='utf-8', mode='a', index=False)
          #pass

def create_vectors_objects(data):
     '''
     Parameters
     ----------
     @data: array
          the elements of array are the users's feedbacks (type: dictionary)

     Return
     ----------
     array:
          the elements of array are the objects (type: dictionnary) for Learning Model
     array:
          the metrics of the objects for Learning Model
     array:
          the elements of array arte the name of motif 
     '''
     X = []
     no = []
     data_copy = copy.deepcopy(data)
     array_dict = []
     vectors = []
     idxmotif = None
     for d in data_copy:
          tmp = d['items'].copy()
          del d['items']
          result = dict(d, **tmp)
          if 'id' in result:
               result.pop('id', None)
          if 'cover' in result:
               result.pop('cover', None)
          tr = OrderedDict(sorted(result.items()))
          z = list(tr.values())
          idxmotif = list(tr.keys()).index('motif')
          array_dict.append(result)
          #vectors.append(list(tr.values()))
          no.append(str(z[idxmotif]))
          del z[idxmotif]
          X.append(z)
     X = np.array(X)
     return array_dict, X, no
















