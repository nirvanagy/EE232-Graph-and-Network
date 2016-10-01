# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 15:50:40 2016

@author: lijiahui
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
    
##filter the actresses file
for line in actresses:
    x = Seperate(line)# all the movies for an actress
    act_to_movie[id]=[]
    act_to_movie[id] = x
    id = id+1
    
"""To get movie to actor"""    
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
            #node_to_movie.write(str(m_id) + '\t\t' + str(key) + '\n')
            m_id = m_id+1            


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

movie_rating=open('/Users/lijiahui/Desktop/Prj2/project_2_data/movie_rating.txt','r')                
movie_to_rating={}
for line in movie_rating:
    count1= line.find(')')+1
    count2= line.find('\t')+2
    count3= line.find('\n')-1
    movie_to_rating[line[0:count1]]= line[count2:count3]

    
Top5_1=[110812,93759,41046,11425,20481]
Top5_2=[85861,61285,56157,140759,1360]
Top5_3=[134498,19963,130390,131807,105343]
Top5_rating1=[]
Top5_rating2=[]
Top5_rating3=[]

for i in range(len(Top5_1)):
    if find_name_with_id.has_key(Top5_1[i]):
        print find_name_with_id[Top5_1[i]]
        temp1=find_name_with_id[Top5_1[i]]
        if (movie_to_rating.has_key(temp1)):
            Top5_rating1.append(float(movie_to_rating[temp1]))
print 'end1'
    
    
for i in range(len(Top5_2)):
    if find_name_with_id.has_key(Top5_2[i]):
        print find_name_with_id[Top5_2[i]]
        temp2=find_name_with_id[Top5_2[i]]
        if (movie_to_rating.has_key(temp2)):
    
            Top5_rating2.append(float(movie_to_rating[temp2]))
            
print 'end2'
for i in range(len(Top5_3)):
    if find_name_with_id.has_key(Top5_3[i]):
        print find_name_with_id[Top5_3[i]]
        temp3=find_name_with_id[Top5_3[i]]
        if (movie_to_rating.has_key(temp3)):
    
            Top5_rating3.append(float(movie_to_rating[temp3]))
            
#rate1=sum(Top5_rating1)/len(Top5_rating1)
#rate2=sum(Top5_rating2)/len(Top5_rating2)
#rate3=sum(Top5_rating3)/len(Top5_rating3)
'''Minions = 6.4 Mission impossiable = 7.5 Batman =7.1 '''

#Eloise (2015)
#Into the Storm (2014) 5.9
#The End of the Tour (2015) 7.8
#Grain (2015) 
#Man of Steel (2013) 7.2


#Fan (2015)
#Phantom (2015) 5.6
#The Program (2015/II) 6.5
#Breaking the Bank (2014) 8.6
#Legend (2015/I) 7.0
Top5_rating2[0:3]=[5.6, 6.5,8.6,7.0]



#
#The Lorax (2012)
#Inside Out (2015)
#Despicable Me 2 (2013)
#Up (2009)
#Surf's Up (2007)
Weight=[6,0.1,0.1,0.4,0.4]
Weight=[5,4,3,2,1]
rate1=Weight[1]*Top5_rating1[0] + Weight[2]*Top5_rating1[1]+Weight[4]*Top5_rating1[2] 
rate1=rate1/(Weight[1]+Weight[2]+Weight[4])
rate2=Weight[1]*Top5_rating2[0] + Weight[2]*Top5_rating2[1] +Weight[3]*Top5_rating2[2] +Weight[4]*Top5_rating2[3] 
rate2=rate2/(Weight[1]+Weight[2]+Weight[3]+Weight[4])
rate3=Weight[0]*Top5_rating3[0] + Weight[1]*Top5_rating3[1] +Weight[2]*Top5_rating3[2]+Weight[3]*Top5_rating3[3]+Weight[4]*Top5_rating3[4] 
rate3=rate3/(Weight[0]+Weight[1]+Weight[2]+Weight[3]+Weight[4])
