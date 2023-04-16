library(geodetector)
Data<-read.csv("/output/[3]HSI_IF_Classification.csv.csv")

factor_detector(3,c(4,5,7,8,9,10,11,12),Data)
interaction_detector(3,c(4,5,7,8,9,10,11,12),Data)