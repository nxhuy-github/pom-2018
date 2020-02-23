from scipy.spatial import distance_matrix
import numpy as np
from collections import defaultdict

def add_score(scores, X):
     keys = []
     matrix = []
     for x in X:
          key = x['motif']
          score = scores[str(key)]
          vf = get_metrics_values_features(x)
          vf.append(score) # the last element is the score
          matrix.append(vf)
          keys.append(str(key))
     #matrix = np.array(matrix)
     return matrix, keys

def get_metrics_values_features(x):
     ordered = sorted(x.keys())
     r = []
     for o in ordered:
          if o != 'motif':
               r.append(x[o])
     return r

def find_idmax(matrix):
     vmax = matrix[0][-1]
     idmax = 0
     for i in range(1, len(matrix)):
          if vmax < matrix[i][-1]:
              vmax =  matrix[i][-1]
              idmax = i
     return idmax

def topScore(scores, nb, X):
     tmp = sorted(scores.items(), key=lambda x: x[1], reverse=True)
     _X = []
     topScore = {}
     for i in range(0, nb):
          key = tmp[i][0]
          value = tmp[i][1]
          topScore[key] = value
     keys = list(topScore.keys())
     for x in X:
          if str(x['motif']) in keys:
               _X.append(x)
     return topScore, _X

def MMR(matrix, Q):
     mmrs = []
     alpha = .5
     for row in matrix:
          quality = row[-1]
          _X = np.array([row[:-1]])
          _Y = np.array(Q)
          d = distance_matrix(_X, _Y)
          d_min = d[np.unravel_index(np.argmin(d), d.shape)]
          mmr = alpha * quality + (1 - alpha)*d_min
          #print('Score: %s, Q: %s' %(quality, Q))
          #print('==================================')
          mmrs.append(mmr)
     idx = np.argmax(mmrs)
     #print('MMRS: ', np.array(mmrs))
     #print('IDX: ', idx)
     return idx

def MMR2(matrix, Q):
     alpha = .5
     qualities = [row[-1] for row in matrix]
     X = np.array([row[:-1] for row in matrix])
     Y = np.array(Q)
     d = distance_matrix(X, Y)
     d_min = [r[np.argmin(r)] for r in d]
     mmrs = [alpha*qualities[i] + (1-alpha)*dm for (i, dm) in enumerate(d_min)]
     idx = np.argmax(mmrs)
     #print('MMRS: ', np.array(mmrs))
     #print('IDX-MMR2: ', idx)
     return idx

def diversity(scores, X, sizeQ):
     #top10, _X = topScore(scores, 10, X)
     matrix, keys = add_score(scores, X)
     Q = []
     results = []
     idmax = find_idmax(matrix)
     results.append(keys[idmax])
     Q.append(matrix[idmax][:-1])
     matrix = np.delete(matrix, idmax, 0)
     del keys[idmax]

     for i in range(0, sizeQ-1):
          idx = MMR(matrix, Q)
          #idx = MMR2(matrix, Q)
          results.append(keys[idx])
          Q.append(matrix[idx][:-1].tolist())       
          matrix = np.delete(matrix, idx, 0)
          del keys[idx]
     return results
