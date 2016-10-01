# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:48:51 2016

@author: Yeziyun
"""

movieid = open('C:/Users/Yeziyun/Desktop/node_to_movie0602.txt', 'r')
moviegenre = open('C:/Users/Yeziyun/Desktop/movie_genre.txt', 'r')
genre_sort_byid = open('C:/Users/Yeziyun/Desktop/genre_sort_byid.txt', 'w')

id_to_movie = {};
movie_to_genre={};

for line in movieid:
    count1 = line.find('\t')
    id_to_movie[line[0:count1]]=line[count1+2:len(line)-1]

for line in moviegenre:
    count1 = line.find('\t')
    movie_to_genre[line[0:count1]]=line[count1+2:len(line)-1]
    
for i in range(140834):
    name = id_to_movie[str(i)]
    if(movie_to_genre.has_key(name)):
        genre = movie_to_genre[name]
        genre_sort_byid.write(genre+'\n')
    else:
        genre_sort_byid.write('null'+'\n')

movieid.close()
moviegenre.close()
genre_sort_byid.close()
    