#!/usr/local/bin/Rscript

args=commandArgs(trailingOnly=TRUE) #save name of csv file from stdin and read
elements <-read.csv(paste(args[1],".csv",sep=""),header=FALSE)
agg=aggregate(elements$V1,by=list(elements$V3),FUN=sum) #find total per category
pdf(file=paste(args[1],".pdf",sep="")) #create pdf and make barplot
p<-barplot(agg$x,main="Spending Data",xlab="Category",ylab="Amount",cex.names=0.8,names=agg$Group.1)

text(x=p,y=agg$x,label=agg$x,pos=1)
dev.off()
