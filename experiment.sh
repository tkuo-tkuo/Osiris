#!/bin/bash/

# $1 is number of required paths
paths=$(python paths_extract.py -n $1)
# echo $paths 

Field_Separator=$IFS
IFS=,
counter=1
for path in $paths; do 
	echo $counter/$1
	source ./runOsiris.sh "$path" OEC "-m strong" > experiments/$counter.txt
	((counter++))
done 

IFS=$Field_Separator

