# -*- coding: utf-8 -*-
"""
Created on Wed May 25 23:57:20 2016

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
            return all_movies
        all_movies.append(line[count1 + 2:count3+1])    


#Repeat Problem number1
actors = open('/Users/lijiahui/Desktop/Prj2/project_2_data/actor_movies.txt', 'r')
actresses = open('/Users/lijiahui/Desktop/Prj2/project_2_data/actress_movies.txt', 'r')

act_to_movie = {};
movie_to_actor={};

id = 0
for line in actors:
    x = Seperate(line)# all the movies for an actor
    act_to_movie[id]=[]
    act_to_movie[id]=x
    id = id+1
    
#filter the actresses file
for line in actresses:
    x = Seperate(line)# all the movies for an actress
    act_to_movie[id]=[]
    act_to_movie[id] = x
    id = id+1
    
"""To get movie to actor dictionary"""    
actors = open('/Users/lijiahui/Desktop/Prj2/project_2_data/actor_movies.txt', 'r')
actresses = open('/Users/lijiahui/Desktop/Prj2/project_2_data/actress_movies.txt', 'r')

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
    
    
node_to_movie = open('node_to_movie0602.txt','w') 
#find the more than five acotrs
m_id = 0#movie id for movie with # of actors > 4
find_mid_with_name = {} #use name to search the id of this moive
find_name_with_id = {} #use id to search the movie name
movie_to_actor5={}    
for key in movie_to_actor:
    if(len(movie_to_actor[key])>14):
        if(key!=''):
            movie_to_actor5[key] =[]
            movie_to_actor5[key] =movie_to_actor[key]
            find_mid_with_name[key]=m_id #give name, value is its id
            find_name_with_id[m_id] = key #give id, value is name of movie
            node_to_movie.write(str(m_id) + '\t\t' + str(key) + '\n')
            m_id = m_id+1
            
node_to_movie.close()

#find intersection   
movie_intersect={}
for key in movie_to_actor5:
    movie_intersect[key]=[]# every movie 
    act = movie_to_actor5[key]   #the actor of that movie 
    for i in range(len(act)):  
        mov =  act_to_movie[act[i]]    #movie of every actor
        for j in range(len(mov)):    
            if (mov[j]==key):      #skip actor himself
                j = j+1
            else:
                movie_intersect[key].append(mov[j])
             
#weight={}
movie_weights=open('movieweight60.txt', 'w')
flg=1
for key in movie_to_actor5:
    num_of_actors_in_movie = len(movie_to_actor5[key])
    id_of_this_movie = find_mid_with_name[key]
    temp_intersect=movie_intersect[key]
    temp_len_intersect=len(temp_intersect)
    for k in range(temp_len_intersect):
        if(temp_intersect[k]!="-1"):       #-1 means we have calculated the weight between these movies
            common_movie = temp_intersect[k]
            if (movie_to_actor5.has_key(common_movie)):                
                if(find_mid_with_name[common_movie] > id_of_this_movie): #only check the movie with id>this movie to avoid repeating           
                    count = 0
                    for rem in range( k,temp_len_intersect ): #look at remaining part
                        if( temp_intersect[rem] == common_movie):#this node is also counted
                            count =count+1
                            temp_intersect[rem] = "-1" #mark this movie as visited
                    if(count>0):
                        weight=float(count)/( num_of_actors_in_movie + len(movie_to_actor5[common_movie]) - count) #definition of Jaccard Index
                    #write find_mid_with_name[key], find_mid_with_name[common_movie], weight to graph file
                        movie_weights.write(str(id_of_this_movie) + '\t\t' + str(find_mid_with_name[common_movie]) + '\t\t' + str(weight)+ '\n')
    print flg#count the number of iterations
    flg=flg+1    
movie_weights.close()