#Fast Greedy
moviegraph<-read.graph("/Users/lijiahui/Desktop/EE232/movieweight60.txt", format = c("ncol"),directed = FALSE)
movie_com<-fastgreedy.community(moviegraph)


#plot the community with color
#comps <- movie_com$membership
#colbar <- rainbow(max(comps)+1)
#V(moviegraph)$color <- colbar[comps+1]
#plot(moviegraph,  vertex.size=5, vertex.label=NA)

#Tag communities

#read the movie genre
genrefile <- file("/Users/lijiahui/Desktop/Prj2/project_2_data/genre_sort_byid.txt",open = "r")
lines <- readLines(genrefile)
close(genrefile)


#assign the genre attribute to each node of the graph
V(moviegraph)$genre = lines[as.numeric(V(moviegraph)$name)+1]
## tag the communtiy with genre that appear more than 20% in the community
com_tag = numeric(0)
for (i in 1:length(movie_com)){ #for each community
  com_genre = V(moviegraph)[which(movie_com$membership ==i)]$genre  #all genres in that community
  max = 0
  max_index = "null"
  genre_type = unique(com_genre) #unique genres
  for(gen in genre_type) #for each gen
  {
    if(length(which(com_genre == gen))>=max && length(which(com_genre == gen))>=length(com_genre)*0.2 && gen!="null")
    {
      max = length(com_genre[which(com_genre == gen)])
      max_index = gen
    }
  }
  if(max_index=="null")
    print("There is no genre appearing more than 20%")
  else{
    cat(i,"\t",max_index,"\n")
    com_tag = c(com_tag,max_index)
  }
}

#calculate the number of each tag of communities
length(which(com_tag=="Drama"))