# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 23:29:24 2014

@author: BAJAJ
"""
from __future__ import print_function
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
from time import time

import numpy as np


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


def nnalgo(X):
    nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(X)
    distances, indices = nbrs.kneighbors(X)
    return [distances,indices]
    

print("Loading Data from database")

from database import getdataset

sql="SELECT * FROM news ORDER BY RAND()"
dataset=getdataset(sql)



print("%d documents" % len(dataset.data))
print("%d categories" % len(dataset.target_names))
print()

print("Extracting features from the training dataset using a sparse vectorizer")
t0 = time()

#max no of features
n_features=10000
use_idf=True

vectorizer = TfidfVectorizer(max_df=0.6
, max_features=n_features,
                                 stop_words='english', use_idf=use_idf)
  
from stemming import *

stems(dataset)
                              
X = vectorizer.fit_transform(dataset.data)

print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X.shape)
print()

#nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X)
'''nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(X)
distances, indices = nbrs.kneighbors(X)
'''
distances, indices=nnalgo(X)

from cluster_fun import cluster_code

cluster=cluster_code(dataset,distances,indices,dowrite=False)

cluster_no=cluster.cluster_no
clust_dict_main=cluster.clust_dict

clust_list_main=cluster.clust_list
del clust_list_main[0]


''' classification for news here starts here  '''


from classfication import *

from database import getempty

dataset_tech=getempty()#2
dataset_health=getempty()#0
dataset_business=getempty()#3
dataset_science=getempty()#1\

def adddata(dat,i):
    (dat.data).append(dataset.data[i])
    (dat.headline).append(dataset.headline[i])
    (dat.link).append(dataset.link[i])
    (dat.photo_id).append(dataset.photo_id[i])
    (dat.source).append(dataset.source[i])
    (dat.short_description).append(dataset.short_description[i])
    (dat.date).append(dataset.date[i])
    
for i in range(0,len(dataset.data)):
    if dataset.target[i]==0:
        adddata(dataset_health,i)
    if dataset.target[i]==1:
         adddata(dataset_science,i)
    if dataset.target[i]==2:
        adddata(dataset_tech,i)
    if dataset.target[i]==3:
        adddata(dataset_business,i)

vectorizer_business = TfidfVectorizer(max_df=0.5
, max_features=n_features,
                                 stop_words='english', use_idf=use_idf)
X_health=vectorizer.fit_transform(dataset_health.data)
X_business=vectorizer_business.fit_transform(dataset_business.data)
X_science=vectorizer.fit_transform(dataset_science.data)
X_tech=vectorizer.fit_transform(dataset_tech.data)

distances_tech, indices_tech=nnalgo(X_tech)
distances_health, indices_health=nnalgo(X_health)
distances_business, indices_business=nnalgo(X_business)
distances_science, indices_science=nnalgo(X_science)

cluster=cluster_code(dataset_tech,distances_tech,indices_tech,dowrite=False)
clust_dict_tech=cluster.clust_dict
clust_list_tech=cluster.clust_list
del clust_list_tech[0]

cluster=cluster_code(dataset_health,distances_health,indices_health,dowrite=False)
clust_dict_health=cluster.clust_dict
clust_list_health=cluster.clust_list
del clust_list_health[0]

cluster=cluster_code(dataset_business,distances_business,indices_business,dowrite=False)
clust_dict_business=cluster.clust_dict
clust_list_business=cluster.clust_list
del clust_list_business[0]

cluster=cluster_code(dataset_science,distances_science,indices_science,dowrite=False)
clust_dict_science=cluster.clust_dict
clust_list_science=cluster.clust_list
del clust_list_science[0]


import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self,cat):
        if(cat=='main'):
            self.render("HomePage.html", clust=clust_list_main, dataset=dataset,tit="Top stories")
        if(cat=='tech'):
            self.render("HomePage.html", clust=clust_list_tech, dataset=dataset_tech,tit="Technology")
        if(cat=='health'):
            self.render("HomePage.html", clust=clust_list_health, dataset=dataset_health,tit="Health")
        if(cat=='business'):
            self.render("HomePage.html", clust=clust_list_business, dataset=dataset_business,tit="Business")
        if(cat=='science'):
            self.render("HomePage.html", clust=clust_list_science, dataset=dataset_science,tit="Science")
            
    def css_files(self):
        return ["HomePage.css"]
        

settings = {
"static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/news/(.*)", MainHandler),],**settings
)

if __name__ == "__main__":
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
