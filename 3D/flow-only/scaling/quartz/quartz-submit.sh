#!/bin/bash

number_of_nodes=("1" "2" "4" "8" "16" "32" "64" "128" "256" "512")

for nnode in ${number_of_nodes[@]}; do
    nproc=$(echo "$nnode*36" | bc)
    fname="run.$nnode.$nproc.out"
    echo "Submitting job for $nnode nodes, $nproc mpi tasks"

    # first job has no dependency... rest wait until previous finished
    if [[ -z $jobid ]]; then
        out=$(sbatch --nodes=$nnode --ntasks=$nproc -o $fname slurm.N.job)
    else
        out=$(sbatch --dependency=afterok:$jobid --nodes=$nnode --ntasks=$nproc -o $fname slurm.N.job)
    fi
    jobid=$(echo $out | sed 's/Submitted batch job //')
done

