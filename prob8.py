# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 10:35:05 2016

@author: YangG
"""

class node:
    name = ''
    values = None
    
def Seperate(line):
    all_movies = []
    count1 = 0
    count2 = 0
    while True:
        count1 = line.find('\t', count2)#first tab
        count2 = line.find('\t', count1 + 2)#next tab
        count3=line.find(')',count1)
        if(count2 == -1):
            all_movies.append(line[count1 + 2:count3+1])   
#            if (line[len(line)-2]!=')' and line[len(line)-2]!='}'):
#                all_movies.append(line[count1 + 2:len(line) - 3])
#            else:
#                all_movies.append(line[count1+2:len(line)-1])
            return all_movies
        all_movies.append(line[count1 + 2:count3+1])    

"""To get movie to actor"""    
actors = open('/Users/YangG/Desktop/232_final/actor_movies.txt', 'r')
actresses = open('/Users/YangG/Desktop/232_final/actress_movies.txt', 'r')
movie_to_actor={};

id2=0
for line in actors:
    x = Seperate(line)# all the movies for an actor
    for movie in x:
        if (movie_to_actor.has_key(movie)==False):
            movie_to_actor[movie]=[]
        movie_to_actor[movie].append(id2)
    id2 =id2 +1

for line in actresses:
    x = Seperate(line)
    for movie in x:
        if (movie_to_actor.has_key(movie)==False):
            movie_to_actor[movie]=[]
        movie_to_actor[movie].append(id2)
    id2 =id2 +1
    

#find the more than five acotrs
m_id = 0#movie id for movie with # of actors > 4
find_mid_with_name = {} #use name to search the id of this moive
find_name_with_id = {} #use id to search the movie name
movie_to_actor5={}    
for key in movie_to_actor:
    if(len(movie_to_actor[key])>4):
        if(key!=''):
            movie_to_actor5[key] =[]
            movie_to_actor5[key] =movie_to_actor[key]
            find_mid_with_name[key]=m_id #give name, value is its id
            find_name_with_id[m_id] = key #give id, value is name of movie
            m_id = m_id+1

#prob 8
import csv
import numpy as np

#movienames
fields=[]
for key in movie_to_actor5:
    templist=[]
    templist.append(key)
    fields.append(templist)
#----csv
movienames=file('movienames.csv','wb')
writer=csv.writer(movienames)
#writer.writerow(dict(zip(FIELDS, FIELDS)))  
writer.writerows(fields)
movienames.close()   

#top5 pagerank of movie 
actor_pagerank={}
with open('/Users/YangG/Desktop/232_final/project_2_data/pageranknew.csv', 'r') as f:
    reader = csv.reader(f)
    #data_list = [row for row in reader]
    for row in reader:
        actor_pagerank[int(row[0])]=row[1]
    # all the data in np.array format
    #data =int(data_list)
    f.close()
  
movie5pagerank=np.zeros([len(movie_to_actor5),5])
j=0
for key in movie_to_actor5: 
    #movie5pagerank[i,0]=i
 actor_id=movie_to_actor5[key]
 temp_rank=[]
 for i in range(len(actor_id)):
     if actor_pagerank.has_key(actor_id[i]):
         temp_rank.append(np.float(actor_pagerank[actor_id[i]]))
         top5rank=sorted(temp_rank,reverse=True)[0:5]
 movie5pagerank[j,0:len(top5rank)]=top5rank
 j=j+1
 
#----csv
movie5ranks=file('movie5ranks.csv','wb')
writer=csv.writer(movie5ranks)
#writer.writerow(dict(zip(FIELDS, FIELDS)))  
writer.writerows(movie5pagerank)
movie5ranks.close()   


#ratings
ratings = open('/Users/YangG/Desktop/232_final/movie_rating.txt', 'r')
movie_ratings={}
for line in ratings:
    count1 = line.find('\t')
    movie_ratings[line[0:count1]]=np.float(line[count1+2:len(line)-2])

movie5ratings=np.zeros([len(movie_to_actor5),1])
m=0
countmiss=0
for key in movie_to_actor5:
    if movie_ratings.has_key(key):movie5ratings[m,0]=movie_ratings[key]
    elif len(key)<2:print m,key
    elif(not key[-2].isdigit()):
        countmiss=countmiss+1 
        print m,key
    m=m+1
#----csv
movie5ratingscsv=file('movie5ratings.csv','wb')
writer=csv.writer(movie5ratingscsv)
#writer.writerow(dict(zip(FIELDS, FIELDS)))  
writer.writerows(movie5ratings)
movie5ratingscsv.close()   


#top100 directors
topdirmovies= open('/Users/YangG/Desktop/232_final/TopDirMov.txt', 'r')
topdir=np.zeros([len(movie_to_actor5),1])
topmvslist={}
for line in topdirmovies:
    count=line.find(')')
    topmvslist[line[0:count+1]]=1

n=0
for key in movie_to_actor5:
    if topmvslist.has_key(key):topdir[n,0]=1
    n=n+1

#----csv
movietopdir=file('movietopdir.csv','wb')
writer=csv.writer(movietopdir)
#writer.writerow(dict(zip(FIELDS, FIELDS)))  
writer.writerows(topdir)
movietopdir.close() 

#genre average ratings
genra = open('/Users/YangG/Desktop/232_final/movie_genre.txt', 'r')
movie_genra={}
for line in genra:
    count1 = line.find('\t')
    movie_genra[line[0:count1]]=line[count1+2:len(line)-2]

nogen=0    
movie5genre={}
for key in movie_to_actor5:
    if (movie_genra.has_key(key)):
        movie5genre[key]=movie_genra[key]
    else:
        nogen=nogen+1
        print key
        movie5genre[key]=''
        
genrescore={}
for key in movie_genra:
    if(not genrescore.has_key(movie_genra[key])):
        genrescore[movie_genra[key]]=[]
        if(movie_ratings.has_key(key)):
            genrescore[movie_genra[key]].append(movie_ratings[key])
            genrescore[movie_genra[key]].append(1)
        else:
            genrescore[movie_genra[key]].append(0)
            genrescore[movie_genra[key]].append(0)        
    else:
         if(movie_ratings.has_key(key)): 
             genrescore[movie_genra[key]][0]=genrescore[movie_genra[key]][0]+movie_ratings[key]
             print genrescore[movie_genra[key]][0]
             genrescore[movie_genra[key]][1]=genrescore[movie_genra[key]][1]+1
             
genreave={}
for key in genrescore:
    if (genrescore[key][1]>0):
        genreave[key]=genrescore[key][0]/genrescore[key][1]
        
movie5genreave=np.zeros([len(movie_to_actor5),1])
k=0
for key in movie_to_actor5:
    if(genreave.has_key(movie5genre[key])):
        movie5genreave[k,0]=genreave[movie5genre[key]]
    k=k+1

        
#----csv
moviegenave=file('moviegenave.csv','wb')
writer=csv.writer(moviegenave)
#writer.writerow(dict(zip(FIELDS, FIELDS)))  
writer.writerows(movie5genreave)
moviegenave.close() 