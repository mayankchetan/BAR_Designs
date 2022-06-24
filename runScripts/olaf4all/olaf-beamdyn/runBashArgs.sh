#!/bin/bash


function runOFjobs (){

    for i in {3..25}
    do
        echo "Running $1 at $i m/s on $2 core(s)"
        sbatch --job-name=${1}_${i}_olaf_bd --output=logs/%j.${1}_${i}_olaf_bd.log ${1}ArgBasedScript.sh $i $i $2
        sleep 1
    done

}

numCores=1

############ 
TURB='usc'
runOFjobs $TURB $numCores

############ 
TURB='urc'
runOFjobs $TURB $numCores

############ 
TURB='drc'
runOFjobs $TURB $numCores
