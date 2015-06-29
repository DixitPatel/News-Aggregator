# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 19:25:11 2014

@author: BAJAJ
"""

from nltk.stem.porter import PorterStemmer

ptstem=PorterStemmer()

def stems(dataset):
    for i in range(0,len(dataset.data)):
        stri=""
        for token in (dataset.data[i]).split():
            stri=stri+" "+ptstem.stem(token)
        dataset.data[i]=stri
    