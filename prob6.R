#Do fast greedy again or use results in prob.5
#moviegraph<-read.graph("/Users/lijiahui/Desktop/EE232/movieweight60.txt", format = c("ncol"),directed = FALSE)
#movie_com<-fastgreedy.community(moviegraph)


newMovie<-c("Batman v Superman: Dawn of Justice (2016)","Mission: Impossible - Rogue Nation (2015)","Minions (Voice) (2015)")
newMovie<-c(80773,125230,87353)
for(k in 1:3)
{
  newNode<-which(V(moviegraph)$name==newMovie[k])
  incidents<-incident(moviegraph,newNode)
  neighbors<-neighbors(moviegraph,newNode)
  if(length(neighbors)>5)
  {
    weights<-E(moviegraph)[incidents]$weight
    weightSort<-sort(weights,index.return=T,decreasing=T)
    top5index<-weightSort$ix[1:5]
    top5<-neighbors[top5index]
  }
  else
  {
    top5<-neighbors
  }
  print(newMovie[k])
  print(movie_com$membership[newNode])
  print(top5)# find movie name 
  print(movie_com$membership[top5])
}
