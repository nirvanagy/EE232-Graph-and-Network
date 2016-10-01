movies=read.csv(file("/Users/YangG/Desktop/232_final/project_2_data/movienames.csv"),header=FALSE,fileEncoding="latin1")
pageranks=read.csv( file("/Users/YangG/Desktop/232_final/project_2_data/movie5ranksnew.csv"), header=FALSE,col.names = c('pr1','pr2','pr3','pr4','pr5'))
ratings=read.csv( file("/Users/YangG/Desktop/232_final/project_2_data/movie5ratings.csv"), header=FALSE)
topdirs=read.csv( file("/Users/YangG/Desktop/232_final/project_2_data/topdir101.csv"), header=FALSE)
genave=read.csv( file("/Users/YangG/Desktop/232_final/project_2_data/moviegenave.csv"), header=FALSE,col.names = 'genave')
ranksanddirs=cbind(topdirs,pageranks,genave,row.names=movies[,1])
rownames(ratings)<-movies[,1]

library("caret", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")

withratingidx=which(ratings>0)
datasetX=ranksanddirs[withratingidx,]
datasetY=ratings[withratingidx,]
withgenaveidx=which(datasetX$genave>0)
datasetX2=datasetX[withgenaveidx,]
datasetY2=datasetY[withgenaveidx]

#datasetX2,Y2 are samples available for training
predictidx=c(which(row.names(ranksanddirs)=='Mission: Impossible - Rogue Nation (2015)'), which(row.names(ranksanddirs)=='Minions (2015)'),which(row.names(ranksanddirs)=='Batman v Superman: Dawn of Justice (2016)'))
predictX1<-ranksanddirs[predictidx,]#without factor


#Sampling1
#To predict the movie ratings from the same population, taking a simple random sample of the data would be appropriate.
#modelX<-datasetX[-predictidx,]
#modelY<-datasetY[-predictidx]
inTrain<-createDataPartition(datasetY2,p=0.1)
TrainX<-datasetX2[unlist(inTrain),]
TrainY<-datasetY2[unlist(inTrain)]
logTrainY<-log(TrainY)
twoTrainY<-2^(TrainY)
versTrainY<-(TrainY)^(-1)

# Sampling2:topdir=nontopdir=1000
withTopdir=which(datasetX2$V101==0)
newTrainXpart1<-datasetX2[withTopdir,]
newTrainYpart1<-datasetY2[withTopdir]
withoutTopdirX<-datasetX2[-withTopdir,]
withoutTopdirY<-datasetY2[-withTopdir]

inTrain2<-createDataPartition(withoutTopdirY,p=0.02)
newTrainXpart2<-withoutTopdirX[unlist(inTrain2),]
newTrainYpart2<-withoutTopdirY[unlist(inTrain2)]
newTrainX<-rbind(newTrainXpart1,newTrainXpart2)
newTrainY<-c(newTrainYpart1,newTrainYpart2)

#Sampling3:topdir=nontopdir=10000
inTrain3<-createDataPartition(withoutTopdirY,p=0.05)
newTrainX2part2<-withoutTopdirX[unlist(inTrain3),]
newTrainY2part2<-withoutTopdirY[unlist(inTrain3)]
newTrainY2<-c(rep(newTrainYpart1,5),newTrainY2part2)
newTrainX2<-rbind(newTrainXpart1,newTrainXpart1,newTrainXpart1,newTrainXpart1,newTrainXpart1,newTrainX2part2)

TestdataX<-datasetX2[-unlist(inTrain),]
TestdataY<-datasetY2[-unlist(inTrain)]
inTest<-createDataPartition(TestdataY,p=0.02)
TestX<-TestdataX[unlist(inTest),]
TestY<-TestdataY[unlist(inTest)]


# Data preprocessing
tranRidg<-preProcess(newTrainX2,method = c("BoxCox", "center", "scale","zv"))
newTrainXtrans<-predict(tranRidg,newTrainX2)
rownames(newTrainXtrans)<-NULL
TestXtrans<-predict(tranRidg,TestX)
predictXtrans=predict(tranRidg,predictX1)

#Models&evaluation
set.seed(100)
indx <- createFolds(newTrainY2, returnTrain = TRUE)
ctrl <- trainControl(method = "cv", index = indx)


#1-ridge regression
set.seed(100)
ridgeGrid <- expand.grid(lambda = seq(0, .1, length = 15))
ridgeTune <- train(x =newTrainXtrans, y = newTrainY2,
                   method = "ridge",
                   tuneGrid = ridgeGrid,
                   trControl = ctrl,
                   #preProc = c("center", "scale")
                   )

# significance of predictors
varImp(ridgeTune)

#2-Nerual Network
registerDoMC(10)
nnetGrid <- expand.grid(decay = c(0, 0.01, .1), 
                        size = c(1, 3, 5, 7, 9, 11), 
                        bag = FALSE)

set.seed(100)
nnetTune <- train(x = TrainX2, y = TrainY,
                  method = "avNNet",
                  tuneGrid = nnetGrid,
                  trControl = ctrl,
                  #preProc = c("center", "scale"),
                  linout = TRUE,
                  trace = FALSE,
                  MaxNWts = 13 * (ncol(TrainX2) + 1) + 13 + 1,
                  maxit = 1000,
                  allowParallel = FALSE)

#3-Mars
marsTune <- train(x = newTrainXtrans, y = newTrainY2,
                  method = "earth",
                  tuneGrid = expand.grid(degree = 1, nprune = 2:38),
                  trControl = ctrl)
marsTune
#4-SVM_radial
set.seed(100)
svmRTune <- train(x = newTrainXtrans, y =newTrainY2,
                  method = "svmRadial",
                  #preProc = c("center", "scale"),
                  tuneLength = 10,
                  trControl = ctrl)
svmRTune

#5-random forest
mtryGrid <- data.frame(mtry = floor(seq(10, ncol(newTrainXtrans), length = 10)))
set.seed(100)
rfTune <- train(x = newTrainXtrans, y = newTrainY2,
                method = "rf",
                tuneGrid = mtryGrid,
                ntree = 1000,
                importance = TRUE,
                trControl = ctrl)

#6-#boosting
gbmGrid <- expand.grid(interaction.depth = seq(20, 30, by = 1),
                       n.trees = seq(100, 500, by = 50),
                       shrinkage = c(0.1),n.minobsinnode=10)
set.seed(100)
gbmTune <- train(x =newTrainXtrans, y = newTrainY2,
                 method = "gbm",
                 tuneGrid = gbmGrid,
                 trControl = ctrl,
                 verbose = FALSE)
#7-cubist
cbGrid <- expand.grid(committees = c(1,5,10, 20, 50, 75, 100), 
                      neighbors = c(0, 1, 5, 9))

set.seed(100)
cubistTune <- train(newTrainXtrans,newTrainY2,
                    "cubist",
                    tuneGrid = cbGrid,
                    trControl = ctrl)
#significance of variables
varImp(cubistTune)

#Performances Plots
rownames(TestXtrans)<-NULL
TestPrediciton=predict(cubistTune, TestXtrans)
res=abs(TestPrediciton-TestY)
plot(TestXtrans$genave,TestPrediciton)
x <- c(4,5,6,7,8,9)
y<-c(4,5,6,7,8,9)
abline(lm(y~x),lwd=2, col="red")
plot(TestY,res)

#Prediction
prediction1<-predict(ridgeTune,predictXtrans)
prediction2<-predict(cubistTune,predictXtrans)
