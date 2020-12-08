#!/bin/bash

usageHelp="${0##*/}: Convert L1000 LXB files to text.
Usage: ${0##*/}
-i <filename> LXB file to process (.lxb)
-o <filename> output file [optional], defaults is to replace extension of lxb file with .txt
"

RBIN='R'

LXB2TXTCMD=$(which $0|sed 's/.sh$/.R/')
#LXB2TXTCMD='lxb2txt.r'
badOptionHelp="Option not recognized"

ts=$(date +"%H%M%S");
#required params
datFile=""
#optional params
outfile=""
queue="interactive -Is"
dryrun=0

# Parse command line arguments
while getopts  "i:o:hd" optionName; do
    case "$optionName" in
	i)  
	    if [ -f $OPTARG ]; then 
		infile=$OPTARG
	    else
		echo "File not found: $OPTARG"
		exit 1
	    fi
	    args="$args lxbfile=$infile"
	    ;;
	o)  outfile="$OPTARG"
	    args="$args outfile=$outfile"
	    ;;
	d)  dryrun=1
	    ;;
	h)  echo "$usageHelp"
	    exit 1
	    ;;
	\?) 
	echo "$badOptionHelp"
	echo "$usageHelp"
	exit 1
	;;
    esac
done

if [ "$outfile"xx = "xx" ]; then
    outfile=${infile%.lxb}.txt
    if [ "$outfile" = "$infile" ]; then
	outfile="$infile.txt"
    fi
    args="$args outfile=$outfile"
fi

echo "${0##*/} Parameters:"
echo "outfile: $outfile"
echo "infile: $infile"
echo "-----------------"

# validate arguments
if [ ! -z "$infile" ]; then    
    echo "Running $LXB2TXTCMD..."
    if [ $dryrun -eq 1 ]; then
	echo $RBIN CMD BATCH --slave "--args $args" $LXB2TXTCMD
    else
	$RBIN CMD BATCH --slave "--args $args" $LXB2TXTCMD && echo 'Done'
    fi
else
    echo "Bad arguments"
    echo "$usageHelp"
fi
