# LXB2TXT.R Convert Luminex .lxb files to text
#
# R CMD BATCH --slave '--args lxbfile=<filename> outfile=<filename> savedesc=<integer>' cel2txt.r
#
# Input arguments to script:
# lxbfile: le with list of CEL files to precess (one file per line)
# outfile: output file for gene expression data
# savedesc: integer (0/1) save description of variables [default=0]
# method: normalization method to use, 

args <- commandArgs(TRUE)
nin <- length(args)

#cat (args,nin,"\n")

savedesc=0

if (nin == 2)
  {
    for (a in args) {
      v = strsplit(a, '=')[[1]]
      switch(v[1],
             lxbfile =  infile <- v[2],
	     outfile = outfile <- v[2],
	     savedesc = savedesc <- as.integer(v[2]),
	     cat ("Invalid method specified:",method,"\n")
             )
    }

    cat (infile,outfile,"\n")
    
    library(prada)    
    cat("Reading lxbfile:",infile,"\n")
    ## read cytoframe
    dat<-readFCS(infile)
    
    ## description of variables
    ## description(dat)
    ## select all RID's except 0
    ##keep=which(exprs(dat[,1])!=0)

    ## dump file to text
    cat ("Writing text to:", outfile, "\n")
    write.table(exprs(dat), file=outfile, sep="\t", quote=FALSE, row.names=FALSE)

    ## dump descriptions as well
    if (savedesc == 1) {
	    descfile <- paste(strsplit(outfile,'.txt$'), ".desc", sep="")
	    cat ("Writing desc to:", descfile, "\n")
	    write.table(description(dat), file=descfile, sep="\t", quote=FALSE, row.names=T, col.names=F)
    }
    
  } else
  {
    cat("Invalid Arguments\n")
    cat ("Usage: R CMD BATCH --slave '--args lxbfile=<filename> outfile=<filename> lxb2txt.r\n")
  }

