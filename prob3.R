graph <- read.graph("/Users/lijiahui/Desktop/EE232/weight_prob2.txt", format = c("ncol"), directed=TRUE)
rank <- page.rank(graph)$vector
for(i in 1:length(rank))
{
  print(rank[i])#To find the 10 largest
}
score_Page =sort(rank,decreasing = TRUE)
score_Page[1:10]


