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

actors = open('/Users/lijiahui/Desktop/Prj2/project_2_data/actor_movies.txt', 'r')
actresses = open('/Users/lijiahui/Desktop/Prj2/project_2_data/actress_movies.txt', 'r')

#create new file
type_file=open('/Users/lijiahui/Desktop/Prj2/project_2_data/type_file.txt', 'w')
edge_file=open('/Users/lijiahui/Desktop/Prj2/project_2_data/edge_file.txt', 'w')
movie_to_mid={}

#create files for bipartite graph
id =0
for line in actors:
    if (line.count('\t\t')>1):    
        x = Seperate(line)
        type_file.write('0'+',')
        temp=id
        for movie in x:
            if(movie!=''):
                if (movie_to_mid.has_key(movie)!=True):
                    id=id+1
                    movie_to_mid[movie]=id
                    type_file.write(str('1')+',')
                edge_file.write(str(temp)+','+str(movie_to_mid[movie])+',')
            id=id+1

for line in actresses:
    if (line.count('\t\t')>1):    
        x = Seperate(line)
        type_file.write('0'+',')
        temp=id
        for movie in x:
            if(movie!=''):
                if (movie_to_mid.has_key(movie)!=True):
                    id=id+1
                    movie_to_mid[movie]=id
                    type_file.write(str('1')+',')
                edge_file.write(str(temp)+','+str(movie_to_mid[movie])+',')
            id=id+1            
   
type_file.close()
edge_file.close()
#These two files can be used in R to create bipartite graph


#predicting rating
movie_rating=open('/Users/lijiahui/Desktop/Prj2/project_2_data/movie_rating.txt','r')                
movie_to_rating={}
for line in movie_rating:
    count1= line.find(')')+1
    count2= line.find('\t')+2
    count3= line.find('\n')-1
    movie_to_rating[line[0:count1]]= line[count2:count3]

actors = open('/Users/lijiahui/Desktop/Prj2/project_2_data/actor_movies.txt', 'r')
actresses = open('/Users/lijiahui/Desktop/Prj2/project_2_data/actress_movies.txt', 'r')

ave_rating =open('/Users/lijiahui/Desktop/Prj2/project_2_data/ave_rating.txt','w')
Batman=[]
MissionImpossible=[]
Minions=[]

for line in actors:
    movie_rate=[]
    if (line.count('\t\t')>1): 
        x = Seperate(line)# all the movies for an actor
        isBatman=0
        isMission=0
        isMinions=0        
        for movie in x:
            if(movie!=''):
                if (movie_to_rating.has_key(movie)):
                    movie_rate.append(float(movie_to_rating[movie]))
            if (movie =='Batman v Superman: Dawn of Justice (2016)'):
                isBatman=1
            if (movie =='Mission: Impossible - Rogue Nation (2015)'):
                isMission=1
            if (movie =='Minions (2015)'):
                isMinions=1
#                else:
#                    ave_rating.write(movie+'\n')
        if (len(movie_rate)!=0):
            temp = sum(movie_rate)/len(movie_rate)
            #get the rating of actor for three movies
            if(isBatman==1):
                Batman.append(temp)
            if(isMission==1):
                MissionImpossible.append(temp)
            if(isMinions==1):
                Minions.append(temp)
        else:
            temp =0
        ave_rating.write(line[0:line.find('\t')]+'\t\t'+str(temp)+'\n')
        

for line in actresses:
    movie_rate=[]
    if (line.count('\t\t')>1): 
        x = Seperate(line)# all the movies for an actor
        isBatman=0
        isMission=0
        isMinions=0        
        for movie in x:
            if(movie!=''):
                if (movie_to_rating.has_key(movie)):
                    movie_rate.append(float(movie_to_rating[movie]))
            if (movie =='Batman v Superman: Dawn of Justice (2016)'):
                isBatman=1
            if (movie =='Mission: Impossible - Rogue Nation (2015)'):
                isMission=1
            if (movie =='Minions (2015)'):
                isMinions=1

        if (len(movie_rate)!=0):
            temp = sum(movie_rate)/len(movie_rate)
         #get the rating of actor for three movies   
            if(isBatman==1):
                Batman.append(temp)
            if(isMission==1):
                MissionImpossible.append(temp)
            if(isMinions==1):
                Minions.append(temp)
        else:
            temp =0
        ave_rating.write(line[0:line.find('\t')]+'\t\t'+str(temp)+'\n')
       
ave_rating.close()

Rating_batman=sum(Batman)/len(Batman)
Rating_mission=sum(MissionImpossible)/len(MissionImpossible)
Rating_minions=sum(Minions)/len(Minions)
