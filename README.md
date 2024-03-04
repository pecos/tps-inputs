# tps-inputs
A place to track TPS cases outside the primary code repository.

# Setting up containers
* please read the docker documentation for setting up the containers, https://github.com/pecos/tps/blob/boltzmann-integration/docker/test-gpu/README.md
* Currently BTE batches solver is only tested on Nvidia GPUs, so recommend to use GPU containers

# To run TPS + 0D-BTE code
You should get, 
* tps-inputs in the boltzmann-integration branch https://github.com/pecos/tps-inputs/tree/boltzmann-integration
* BTE solver main branch https://github.com/ut-padas/boltzmann (please let me know (milinda@oden.utexas.edu) if you have any access issues since it is a private repository)
* tps code boltzmann-integration brach https://github.com/pecos/tps/tree/boltzmann-integration

# How to run the TPS + BTE 

Below is to build and run tps with cuda SM_80
```
#!/bin/bash
export CUDA_ARCH=sm_80
cd tps
echo $PWD
source /etc/profile.d/lmod.sh
ml list
#./bootstrap
#mkdir -p build-cpu && cd build-cpu && ../configure --enable-pybind11 && cd ..
#cp src/*.py build-cpu/src/.
#cd build-cpu && make all -j16 && cd ../

mkdir -p build-cuda && cd build-cuda && ../configure --enable-pybind11 --enable-gpu-cuda CUDA_ARCH=$CUDA_ARCH && cd ..
cd build-cuda && make all -j16 && cd ../
cp src/*.py build-cuda/src/.

#echo $PWD
#cd tps-inputs/axisymmetric/argon/lowP/single-rxn
#echo "launching tps + Boltzmann"
#./../../../../../build-cuda/src/tps-time-loop.py -run plasma.reacting.tps2boltzmann.ini
#./../../../../../build-cuda/src/tps-bte_0d3v.py -run plasma.reacting.tps2boltzmann.ini

cd tps-inputs/axisymmetric/argon/lowP/six-species-maxwell-rates
git checkout restart_output-plasma.sol.h5
echo "launching tps + Boltzmann"
#./../../../../../build-cuda/src/tps-time-loop.py -run plasma.reacting.tps2boltzmann.ini
./../../../../../build-cuda/src/tps-bte_0d3v.py -run plasma.6sp.tps2boltzmann.ini
```
  
