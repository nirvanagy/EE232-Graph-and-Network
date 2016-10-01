# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:53:18 2016

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
        if(count2 == -1):
            all_movies.append(line[count1 + 2:len(line) - 3])
            return all_movies
        all_movies.append(line[count1 + 2:count2 - 2])

#Problem number1
actors = open('actor_movies.txt', 'r')
actresses = open('actress_movies.txt', 'r')
movies = open('movies.txt', 'wr')
combined = open('combined.txt', 'w')
weights = open('weight2.txt', 'w')

#lists of actors/actresses with at least 5 movies
all_list   = []

#filter the actors file
for line in actors:
    if(line.count('\t\t') > 4):#at least five movies
        N = node()
        N.name = line[0:line.find('\t')]
        N.values = Seperate(line)
        combined.write(line)
        all_list.append(N)

    
#filter the actresses file
for line in actresses:
    if(line.count('\t\t') > 4):#at least five movies
        N = node()
        N.name = line[0:line.find('\t')]
        N.values = Seperate(line)
        combined.write(line)
        all_list.append(N)

combined = open('combined.txt', 'r')
combined_list=[]
for line in combined:
     combined_list.append(line)
     
#Problem number2
num_nodes = len(all_list)
#calculate all weights, long run-time so write to file for future use
              
for i in range(61075 ,num_nodes):#0 through 244300
    print i
    for j in range(i+1,num_nodes):
        temp = len(set(all_list[i].values).intersection(all_list[j].values))
        if(temp > 0):
            temp1 = float(temp)/len(all_list[i].values)#the edge weight
            temp2 = float(temp)/len(all_list[j].values)
            weights.write(str(i) + '\t\t' + str(j) + '\t\t' + str(temp1)+ '\n')
            weights.write(str(j) + '\t\t' + str(i) + '\t\t' + str(temp2)+ '\n')