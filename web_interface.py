# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 17:29:02 2014


"""
from project_clustering import *

from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

n_components=2

if n_components:
    print("Performing dimensionality reduction using LSA")
    t0 = time()
    lsa = TruncatedSVD(n_components)
    X = lsa.fit_transform(X)
    # Vectorizer results are normalized, which makes KMeans behave as
    # spherical k-means for better results. Since LSA/SVD results are
    # not normalized, we have to redo the normalization.
    #X = Normalizer(copy=False).fit_transform(X)

    print("done in %fs" % (time() - t0))
    print()

import pylab as py

py.plot(X[:,0:1],X[:,1:2],'bo')
py.plot(0.7,0.8,color='c')


import matplotlib.pyplot as plt

colors = ['red', 'green', 'blue','pink','purple','black','grey','yellow']
plt.figure()
plt.xlim([X[0:30,0].min() - .5, X[0:30,0].max() + .5])
plt.ylim([X[0:30,1].min() - .5, X[0:30,1].max() + .5])
plt.xticks([], []); plt.yticks([], []) # numbers aren't meaningful

# show the centroids
#plt.scatter(centroids_2d[:,0], centroids_2d[:,1], marker='o', c=colors, s=100)

# show user numbers, colored by their cluster id
clusterid=clust_dict.values()
for i, ((x,y), kls) in enumerate(zip(X, clusterid[0:30])):
    plt.annotate(str(i), xy=(x,y), xytext=(0,0), textcoords='offset points',
                 color=colors[kls%8])




'''
import tornado.ioloop
import tornado.web
import os



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("HomePage.html", clust=clust_list, dataset=dataset)
    def css_files(self):
        return ["HomePage.css"]
    

settings = {
"static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler),],**settings
)

if __name__ == "__main__":
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
   ''' 