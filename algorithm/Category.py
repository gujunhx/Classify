from sklearn.model_selection import train_test_split
from random import shuffle
import numpy as np
from sklearn import metrics
from sklearn.metrics import classification_report
import pickle
from sklearn.model_selection import ShuffleSplit, KFold
from sklearn.model_selection import GridSearchCV

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import chi2
from sklearn.naive_bayes import MultinomialNB

def getCourps():
    courps = []
    for line in open('prepare_data/data.txt', 'r'):
        courps.append(line)
    shuffle(courps)
    getDataAndLabel(courps)


def getDataAndLabel(courps):
    data = []
    label = []
    for line in courps:
        list = line.split('  ')
        label.append(list[0])
        data.append(list[1])
    X_train, X_val, Y_train, Y_val = train_test_split(data, label, test_size=0.033, random_state=1)
    selectParam(X_train, Y_train)
    # trainModel(X_train, X_val, Y_train, Y_val)



def getTfIdf(train_content):
    vectorizer = CountVectorizer(min_df=20)
    tfidftransformer = TfidfTransformer()
    tfidf = tfidftransformer.fit_transform(vectorizer.fit_transform(train_content))
    print(tfidf.shape)
    return tfidf

def trainModel(X_train, X_val, Y_train, Y_val):

    pipeline = Pipeline([('vect',CountVectorizer(min_df=110, max_df=1000)),
                         ('tfidf', TfidfTransformer()),
                         ('chi', SelectPercentile(chi2,percentile=10)),
                         ('clf', MultinomialNB(alpha=0.0001))])
    pipeline = pipeline.fit(X_train, Y_train)
    # pickle.dump(pipeline, open('model/NB.model','wb'))
    print(X_val[0])
    pre = pipeline.predict(X_val)
    print('NB: ', np.mean(pre == Y_val))
    print(metrics.confusion_matrix(Y_val, pre))
    print(classification_report(Y_val, pre))


def selectParam(X_train, Y_train):
    # cv_split = KFold(n_splits=5)
    cv_split = ShuffleSplit(n_splits=5, train_size=0.8, test_size=0.2)
    param = {'vect__min_df': (100, 200, 300),
             'vect__max_df': (1000, 3000, 5000),
             'chi__percentile': (10, 20, 30),
             'clf__alpha': (0.001, 0.0001, 0.0005),
             }
    pipeline = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('chi', SelectPercentile(chi2)),
                         ('clf', MultinomialNB())])
    grid_search = GridSearchCV(pipeline, param, n_jobs=1, verbose=1, cv=cv_split)
    grid_search.fit(X_train, Y_train)
    print(grid_search.best_score_)
    print(grid_search.best_params_)

getCourps()



