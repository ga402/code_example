#!/bin/sh                                                          

# Example HPC script

#PBS -lselect=1:ncpus=32:mem=248gb
#PBS -lwalltime=02:00:00

export PATH=~/anaconda3/envs/_CONDA_ENV_/bin/:$PATH
source activate _CONDA_ENV_
PBS_O_WORKDIR=/path/script
PROJECT_DIR=path/project/dir
INFILE=_inputfile_
BLOCK_REDUCTION_SIZE=5
OUTFILE=_outfile_.geojson
UTILS_FOLDER=utils

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace
set -o errtrace

cp -r ${PBS_O_WORKDIR}/${UTILS_FOLDER} ${TMPDIR}
# Script
python ${PBS_O_WORKDIR}/createBoundaries.py --file ${PROJECT_DIR}/$INFILE --output $OUTFILE --block_reduce_size $BLOCK_REDUCTION_SIZE

cp -r *${OUTFILE} ${PROJECT_DIR}/

