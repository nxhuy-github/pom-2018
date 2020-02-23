import os, sys, json, numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
from python.boley import random_transaction, extract_motif, weights_transactions, probabilities_transactions
from python.helper import read_csv, cover_coverage_pos_neg, chi_square, items_in_motif, store_data, create_vectors_objects
from python.svmrank import model_ranking, prepare_pairewise_testing_data
from python.svmrank2 import pairewise_testing, ranking
from python.timer import Timer
from python.motif import Motif
from python.mmr import diversity
import pprint

def provide_data_for_web(nbmotif, df, weights):
     '''
     Prepare the data for the user's interface

     Parameters
     ----------
     @nbmotif: int
          the motif's number what we want to choose
     @df: DataFrame
          the data of CSV file
     @items: array
          the column's names of df
     @weights: array
          the weight of each transaction

     Return
     ----------
     array:
          the motifs will be show in the user's interface
     '''
     results = []
     while True:
          rtid = random_transaction(weights)
          motif, metrics, items = extract_motif(df.values[rtid])
          cover, _coverage, pos_c, neg_c = cover_coverage_pos_neg(df.values, metrics)
          #cs = chi_square(cover, weights)

          result = Motif(motif, cover, _coverage, pos_c, neg_c, None, len(motif), items, _coverage*len(motif))

          '''
          result = {
          'motif': motif,
          'cover': cover,
          'coverage': _coverage,
          'pos_cov': pos_c,
          'neg_cov': neg_c,
          'obj_quality': cs,
          'length': len(motif)
          }
          '''
          r = result.toDict()
          del r['cover']
          del r['obj_quality']
          if r not in results:
               results.append(r)
          if len(results) == nbmotif:
               break
     return results
  
def load_data(link, nbmotif):
     '''
     The serveur NodeJS will read the stdout's data, so we will
     print the data (with format JSON) of the user's interface in Python console

     Parameters
     ----------
     @link: string
          path to data file
     
     Return
     ----------
     array:
          the motifs will be show in the user's interface
     '''
     df = read_csv(link)
     items = df.columns.values.tolist()
     weights = weights_transactions(df.values)
     #props = probabilities_transactions(weights)
     results = provide_data_for_web(nbmotif, df, weights)

     resultsJson = json.dumps(results, ensure_ascii=False)
     return results, resultsJson

def calculate_score(y, compares):
     scores = {}
     for (idx, val) in enumerate(y):
          oi, oj = compares[idx].split('-')
          if oi not in scores:
               scores[oi] = 0
          scores[oi] = scores[oi] + np.sign(val)
          if oj not in scores:
               scores[oj] = 0
          scores[oj] = scores[oj] - np.sign(val)
     return scores

def mine(datafile, stored_file_name):
     if os.stat(stored_file_name).st_size == 0:
          nbmotif = 5
          results, resultsJson = load_data(datafile, nbmotif)
          print(resultsJson)
     else:
          nbmotif = 50
          results, resultsJson = load_data(datafile, nbmotif)
          arr, X, no = create_vectors_objects(results)
          Xtest, compares = pairewise_testing(X, no)
          clf, coef = ranking(stored_file_name)
          ytest = clf.predict(Xtest)
          scores = calculate_score(ytest, compares)
          Q = diversity(scores, arr, 5)
          div = []
          for result in results:
               if str(result['motif']) in Q:
                    div.append(result)
          print(json.dumps(div, ensure_ascii=False))
     
def main():
     '''
     Read the command of serveur NodeJS and handle this
     '''
     lines = sys.stdin.readlines()
     data = json.loads(lines[0])
     '''
     data = './public/mushrooms.csv'
     results, _ = load_data(data, 3)
     
     arr, X, no = create_vectors_objects(results)
     Xtest, compares = pairewise_testing(X, no)
     
     link = './public/mushrooms_stored.csv'
     print('Keep waiting...')
     clf, coef = ranking(link)
     ytest = clf.predict(Xtest)
     print(ytest)
     #scores = calculate_score(ytest, compares)
     #print('Length scores:' , len(scores))
     #pp = pprint.PrettyPrinter(indent=4)
     #pp.pprint(scores)
     #print(json.dumps(scores, indent=4, sort_keys=True))
     #Q = diversity(scores, arr, 5)
     #div = []
     #for result in results:
     #     if str(result['motif']) in Q:
     #          div.append(result['motif'])
     #print(div)
     #print(json.dumps(div, ensure_ascii=False))
     '''
     results = []
     vectors_objects = []
     stored_file_name = './public/stored.csv'
     #data = './public/data.csv'
     if data == './public/data.csv':
          stored_file_name = './public/stored.csv'
          mine(data, stored_file_name)
     elif data == './public/mushrooms.csv':
          stored_file_name = './public/mushrooms_stored.csv'
          mine(data, stored_file_name)
     elif data == './public/accidents.csv':
          stored_file_name = './public/accidents_stored.csv'
          mine(data, stored_file_name)
     else:
          try:
               stored_file_name = data.split('&')[0]
               d = json.loads(data.split('&')[1])
               array_dict, _, _ = create_vectors_objects(d)
               store_data(array_dict, str(stored_file_name))
               print('Stored successfully')
          except ValueError as e:
               print(e)
     
     
if __name__ == '__main__':
    main()
