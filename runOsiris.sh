#!/bin/bash/

# Parse parameters from runOsiris.sh to analyse_nb.py
if [ -z "$1" ]
then 
    echo "\$1 is empty. Please indicate proper path to the target Jupyter Notebook file"
    return 
fi 

if [ -z "$2" ]
then 
    echo "$2 is empty. Please indicate one of valid execute strategies (normal/OEC/dependency)"
    return
fi 


FLAG1="-n $1"
FLAG2="-e $2"
FLAG3="$3"
arguments="$FLAG1 $FLAG2 $FLAG3"

# Grab the python version 
py_version=$(python3 grab_py_version.py -n $1 -e $2)

# Switch to appropriate conda environment 
if [ "$py_version" = "3.5" ]
then 
    conda activate Osiris_py35
elif [ "$py_version" = "3.6" ]
then
    conda activate Osiris_py36 
elif [ "$py_version" = "3.7" ]
then
    conda activate Osiris_py37 
elif [ "$py_version" = "2.7" ]
then
    echo "Osiris currently does not implement for python2.7/3.4"
    return 
elif [ "$py_version" = "3.4" ]
then
    echo "Osiris currently does not implement for python2.7/3.4"
    return 
else 
    echo "$py_version"
    return 
fi 

# Run Osiris  
python3 analyse_nb.py $arguments

# exit conda env before leaving shell script 
conda deactivate 


