import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import itertools
from scipy import stats
from python.helper import read_csv
from python.timer import Timer
#from helper import read_csv
#from timer import Timer
import pprint
import time
def filter_feedback(draw_data):
     '''
     In the draw data, if a motif has many feedback(line), we'll use the lastest line for this motif

     Parameters
     ----------
     @draw_data: DataFrame
          the data in CSV file
     
     Return
     ----------
     dictionary:
          key: motif
          value: coverage, items, length, like, etc
     '''
     data = {}
     for row in draw_data.iterrows():
          key = row[1]['motif']
          value = {}
          for (k, v) in row[1].items():
               if k != 'motif':
                    value[k] = v
          data[key] = value
     return data
          
def preprocessing_training_data(link, i):
     '''
     Create the array object(data training) for SVM model

     Parameters
     ----------
     @link: string
          path to feedback file, CSV file
     
     Return
     ----------
     array:
          the objects
     array:
          the targets of objects
     '''
     df = read_csv(link)
     data = filter_feedback(df)
     y = []
     X = []
     names_objects = []
     for (key, value) in data.items():
          names_objects.append(key)
          x = []
          for (k, v) in value.items():
               if k == 'like':
                    y.append(float(v))
               else:
                    x.append(float(v))
          X.append(x)
     X = np.array(X)
     if i != 50:
          X = X[0:i]
          y = y[0:i]
          names_objects = names_objects[0:i]
     return X, y, names_objects

def prepare_pairewise_testing_data(data):
     X = []
     no = []
     for d in data:
          x = []
          for (key, value) in d.items():
               if key != 'motif':
                    x.append(float(value))
               else:
                    no.append(str(value))
          X.append(x)
     X = np.array(X)
     Xtest = []
     compares = []
     comb = itertools.combinations(range(X.shape[0]), 2)
     for (i, j) in comb:
          Xtest.append(X[i] - X[j])
          s = no[i] + '-' + no[j]
          compares.append(s)
     return Xtest, compares

def pairewise_transform(X, y, names_objects):
     '''
     Parameters
     ----------
     @X: array
          the objects for SVM model
     @y: array
          the targets of objects
          
     Return
     ----------
     array:
          the pair-objects for SVM model
     array:
          the targets of pair-objects
     '''
     
     comb = itertools.combinations(range(X.shape[0]), 2)
     k = 0
     X_new, y_new, diff = [], [], []
     compare = []
     for (i, j) in comb:
          if y[i] != y[j]:
               X_new.append(X[i] - X[j])
               diff.append(y[i] - y[j])
               y_new.append(np.sign(diff[-1]))
               if y_new[-1] != (-1)**k:
                   X_new[-1] *= -1
                   y_new[-1] *= -1
                   diff[-1] *= -1
               k += 1
               compare.append(names_objects[i] + '-' + names_objects[j])
     X_new, y_new, diff, compare = map(np.asanyarray, (X_new, y_new, diff, compare))
     return X_new, y_new, compare

def svm_rank(Xp, yp):
     '''
     Use the svm classification with pairwise transform for ranking

     Parameters
     ----------
     @Xp: array
          the pairwise objects for ranking
     @yp: array
          the targets of pairwise objects
          
     Return
     ----------
     array:
          the coefficient of the Ranking model
     '''
     clf = svm.SVC(kernel='linear', C=.1)
     clf.fit(Xp, yp)
     coef = clf.coef_.ravel() / np.linalg.norm(clf.coef_)
     return coef
     

def model_ranking(link, i):
     X, y, names_objects = preprocessing_training_data(link, i)
     Xp, yp , nop= pairewise_transform(X, y, names_objects)
     coef = svm_rank(Xp, yp)
     return coef, len(nop)


    
