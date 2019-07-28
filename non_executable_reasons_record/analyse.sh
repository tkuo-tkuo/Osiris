#!/bin/bash/

input="a.txt"
while IFS= read -r line
do
	cat $line.txt
done < "$input"

