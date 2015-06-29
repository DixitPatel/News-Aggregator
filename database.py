# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 00:29:42 2014


"""
import numpy as np
import MySQLdb

class Bunch(dict):
    """Container object for datasets: dictionary-like object that
       exposes its keys as attributes."""

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self



def getdataset(sql1):
    db=MySQLdb.connect("localhost","root","","python_test")
    
    cursor=db.cursor()
    
    cursor.execute("SELECT VERSION()")
    
    data=cursor.fetchone()
        
   # sql="SELECT * FROM news ORDER BY RAND()"
    
    target = []
    target_names = []
    data=[]
    short_description=[]
    link=[]
    source =[]
    headline=[]
    photo_id=[]
    date=[]

    
    try:
        cursor.execute(sql1)
        results = cursor.fetchall()
        for row in results:
            target.append(row[1])
            headline.append(row[2])
            link.append(row[3])
            source.append(row[4])
            short_description.append(row[5]) 
            data.append(unicode(row[6]))
            date.append(row[7])
            photo_id.append(row[8])
            
    except:
        print("unable to fetch data")
    
    sql="SELECT * FROM category "
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            target_names.append(row[1])
    
    except:
        print("could not fetch data")
    
    db.close()

    target = np.array(target)
   # encoding='unicode'
   # decode_error='strict'
   # data = [d.decode(e, decode_error) for d in data]    
    data=np.array(data)    
        
    return Bunch(target=target,headline=headline,link=link,data=data,
                 short_description=short_description,target_names=target_names, 
                 source=source, photo_id=photo_id,date=date)         


def getempty():
    target = []
    target_names = []
    data=[]
    short_description=[]
    link=[]
    source =[]
    headline=[]
    photo_id=[]
    date=[]
    return Bunch(target=target,headline=headline,link=link,data=data,
                 short_description=short_description,target_names=target_names, 
                 source=source, photo_id=photo_id,date=date)
    