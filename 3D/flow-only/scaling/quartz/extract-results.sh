#!/bin/bash

number_of_nodes=("1" "2")

echo "# (Number of nodes) t0 [sec] t1 [sec]"
for nnode in ${number_of_nodes[@]}; do
    nproc=$(echo "$nnode*36" | bc)
    fname="run.$nnode.$nproc.out"

    t0=$(grep "Iteration = 40" $fname | sed 's/Iteration = 40: wall clock time\/iter = //' | sed 's/ (secs)//')
    t1=$(grep "Iteration = 80" $fname | sed 's/Iteration = 80: wall clock time\/iter = //' | sed 's/ (secs)//')
    echo "$nnode $t0 $t1"
done

