#!/bin/bash
#----------------------------------------------------------------
# convenience wrapper script to launch MPI-based MFEM container
# karl@oden.utexas.edu
#
# Usage: wrap.sh [executable] [args]...
#----------------------------------------------------------------

# initialize modules within container
. /opt/ohpc/admin/lmod/lmod/init/bash
# cleanup module table inherited from host node
clearMT
# restore default ohpc modulepath
export MODULEPATH=/opt/ohpc/pub/modulefiles
# default env for container
module try-add ohpc
module try-add metis
module try-add hypre
module try-add phdf5
module try-add openblas
module try-add ptscotch
module try-add scalapack
module try-add superlu_dist
module try-add petsc
module try-add boost
module try-add gsl

localDir=`dirname $0`
pushd $localDir > /dev/null
#pushd $localDir 

EXE=$1
shift

#ldd $EXE
$EXE "$@"
