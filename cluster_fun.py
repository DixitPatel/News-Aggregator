# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 23:48:07 2014


"""

class Bunch(dict):
    """Container object for datasets: dictionary-like object that
       exposes its keys as attributes."""

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self



import os

def count_files(dir):
    path, dirs, files = os.walk(dir).next()
    file_count = len(files)
    return file_count

def write_file(dir,i,j,dataset,indices):
    f=open(dir,"w")
    f.write(dataset.data[indices[i][j]]) # some encoding error so not used
    # pickle.dump(dataset.data[indices[i][j]],f,1)
    f.close()





def cluster_code(dataset,distances,indices,dowrite=False):
    cluster_no=0
    clust_dict={}   #contains doc no and  cluster into which it is clustered
    
    clust_list=[[]]
    
    clust_list[0]="for html"
    
    for i in range(len(indices)):
        if not clust_dict.has_key(indices[i][0]):
            
            # 1.3 is empirically determined constant
            # check it is only 1 news
            if indices[i][0] not in indices[indices[i][1]] or distances[i][1]>1.2 :
               cluster_no+=1
               dir='C:/ml_datasets/cluster_' + str(cluster_no) +'/' 
               if not os.path.exists(dir):
                  os.makedirs(dir)
               clust_dict[indices[i][0]]=cluster_no
               if dowrite:
                   write_file(dir+'article1.txt',i,0)
               list_test=[]
               list_test.append(indices[i][0])
               clust_list.append(list_test)
             
             # if 1st neighbour is clustered put it in same cluster
            elif clust_dict.has_key(indices[i][1]):
                clust_dict[indices[i][0]]=clust_dict[indices[i][1]]
                dir='C:/ml_datasets/cluster_' +  str(clust_dict[indices[i][1]]) +'/'
                file_count=count_files(dir)
                file_count+=1
                dir=dir+'article'+str(file_count)+'.txt'
                if dowrite:
                    write_file(dir,i,0)
                clust_list[clust_dict[indices[i][1]]].append(indices[i][0])
            # 1st neighbour is not  clustered
            else:
                
                # if there are 2 news
                if distances[i][2]>1.20:          
                   cluster_no+=1
                   dir='C:/ml_datasets/cluster_' + str(cluster_no) +'/' 
                   if not os.path.exists(dir):
                       os.makedirs(dir)
                   clust_dict[indices[i][0]]=cluster_no
                   clust_dict[indices[i][1]]=cluster_no
                   if dowrite:
                       write_file(dir+'article1.txt',i,0)
                       write_file(dir+'article2.txt',i,1)
                   list=[]
                   for j in range(0,2):
                       list.append(indices[i][j])
                   clust_list.append(list)
                
                
                # if there are 3 news
                elif distances[i][3]>1.20:
                   cluster_no+=1
                   dir='C:/ml_datasets/cluster_' + str(cluster_no) +'/' 
                   if not os.path.exists(dir):
                       os.makedirs(dir)
                   clust_dict[indices[i][0]]=cluster_no
                   clust_dict[indices[i][1]]=cluster_no
                   clust_dict[indices[i][2]]=cluster_no
                   if dowrite:
                       write_file(dir+'article1.txt',i,0)
                       write_file(dir+'article2.txt',i,1)
                       write_file(dir+'article3.txt',i,2)
                   list=[]
                   for j in range(0,3):
                       list.append(indices[i][j])
                   clust_list.append(list)
                 # if there are 4 news
                elif distances[i][4]>1.26:
                   cluster_no+=1
                   dir='C:/ml_datasets/cluster_' + str(cluster_no) +'/' 
                   if not os.path.exists(dir):
                       os.makedirs(dir)
                   clust_dict[indices[i][0]]=cluster_no
                   clust_dict[indices[i][1]]=cluster_no
                   clust_dict[indices[i][2]]=cluster_no
                   clust_dict[indices[i][3]]=cluster_no
                   if dowrite:
                       write_file(dir+'article1.txt',i,0)
                       write_file(dir+'article2.txt',i,1)
                       write_file(dir+'article3.txt',i,2)
                       write_file(dir+'article4.txt',i,3)
                   list=[]
                   for j in range(0,4):
                       list.append(indices[i][j])
                   clust_list.append(list)
                # if all 5 news are similar stories
                else:
                   cluster_no+=1
                   dir='C:/ml_datasets/cluster_' + str(cluster_no) +'/' 
                   if not os.path.exists(dir):
                       os.makedirs(dir)
                   clust_dict[indices[i][0]]=cluster_no
                   clust_dict[indices[i][1]]=cluster_no
                   clust_dict[indices[i][2]]=cluster_no
                   clust_dict[indices[i][3]]=cluster_no
                   clust_dict[indices[i][4]]=cluster_no
                   if dowrite:
                       write_file(dir+'article1.txt',i,0)
                       write_file(dir+'article2.txt',i,1)
                       write_file(dir+'article3.txt',i,2)
                       write_file(dir+'article4.txt',i,3)
                       write_file(dir+'article5.txt',i,4)
                   list=[]
                   for j in range(0,5):
                       list.append(indices[i][j])
                   clust_list.append(list)
    return Bunch(cluster_no=cluster_no,clust_dict=clust_dict,clust_list=clust_list)
                  # write for loops for it
        
    
    
    