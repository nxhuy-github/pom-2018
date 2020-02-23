import pandas as pd
import numpy as np
from collections import defaultdict, OrderedDict
import itertools
from sklearn import svm
from scipy.sparse import csr_matrix
import natsort
import pprint
import time
pp = pprint.PrettyPrinter(depth=6)

def transform_to_binary_data(from_, to_):
    df = pd.read_csv(from_, delimiter=' ')
    data = df.dropna(axis=1, how='all').as_matrix()
    mi = data.min()
    ma = data.max()
    d = defaultdict(list)
    d['tid'] = ['t'+str(i) for i in range(1, len(data)+1)]
    for row in data:
        for n in range(mi, ma + 1):
            if n in row:
                d['i'+str(n)].append(1)
            else:
                d['i'+str(n)].append(0)
    keys = natsort.natsorted(d.keys())
    d_new = OrderedDict((k, d[k]) for k in keys)
    df2 = pd.DataFrame(d_new, columns = d_new.keys())
    df2.set_index('tid', inplace=True)
    df2.to_csv(to_)

def get_training_data(file):
    d = defaultdict(list)
    df = pd.read_csv(file)
    df_copy = df.copy()
    motifs = df['motif'].values
    df_copy = df_copy.drop(['motif'], axis=1)
    idcollike = df_copy.columns.get_loc('like')
    array = df_copy.values
    keys = []
    X = []
    y = []
    for (i, cell) in enumerate(array):
        key = motifs[i]
        #keys.append(key)
        #y.append(cell[idcollike])
        #cell = np.delete(cell,idcollike)
        #X.append(cell)
        d[key] = list(cell)
    for (k, v) in dict(d).items():
        keys.append(k)
        y.append(v[idcollike])
        del v[idcollike]
        X.append(v)
    X = np.array(X)
    return X, y, keys

def pairewise_transform(X, y, keys):
    comb = itertools.combinations(range(X.shape[0]), 2)
    k = 0
    Xp, yp, diff = [], [], []
    compare = []
    for (i, j) in comb:
        if y[i] != y[j]:
            Xp.append(X[i] - X[j])
            diff.append(y[i] - y[j])
            yp.append(np.sign(diff[-1]))
            compare.append(str(keys[i]) + '-' + str(keys[j]))
            if yp[-1] != (-1)**k:
                Xp[-1] *= -1
                yp[-1] *= -1
                diff[-1] *= -1
            k += 1
    Xp, yp, diff, compare = map(np.asanyarray, (Xp, yp, diff, compare))
    return Xp, yp, compare

def pairewise_testing(X, no):
    '''
    X = []
    no = []
    for row in array:
        no.append(str(row[idmotif]))
        del row[idmotif]
        X.append(row)
    X = np.array(X)
    '''
    Xtest = []
    compares = []
    comb = itertools.combinations(range(X.shape[0]), 2)
    for (i, j) in comb:
        Xtest.append(X[i] - X[j])
        s = no[i] + '-' + no[j]
        compares.append(s)
    Xtest = np.array(Xtest)
    return Xtest, compares

def ranking(file):
    X, y, no = get_training_data(file)
    Xp, yp, no = pairewise_transform(X, y, no)
    clf = svm.SVC(kernel='linear', C=.1)
    clf.fit(Xp, yp)
    coef = clf.coef_.ravel() / np.linalg.norm(clf.coef_)
    return clf, coef 








