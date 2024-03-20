#!/bin/python3
import configparser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-output_folder" , "--output_folder"           , help="output folder for tps-bte param files", type=str, default="./")
parser.add_argument("-ngpus_per_node", "--ngpus_per_node"          , help="GPUs per node", type=int, default=4)
parser.add_argument("-solver_type"   , "--solver_type"             , help="solver type", type=str, default="steady-state")
parser.add_argument("-out_fname"     , "--out_fname"               , help="output file name for the qois", type=str, default="bte_ss")
parser.add_argument("-lxcat"         , "--lxcat"                   , help="absolute path for lxcat file" , type=str, default="")
parser.add_argument("-sub_clusters"  , "--sub_clusters"            , help="sub cluster size", nargs='+', type=int, default=[1024, 512, 256, 128, 64])
parser.add_argument("-node_count"    , "--node_count"              , help="sub cluster size", nargs='+', type=int, default=[1, 2, 4, 8, 16])

args = parser.parse_args()

output_folder = args.output_folder
base_file     = "plasma.6sp.tps2boltzmann.ini"
lxcat_path    = args.lxcat
sub_clusters  = args.sub_clusters
node_count    = args.node_count

config = configparser.ConfigParser()
config.optionxform=str
config.read(base_file)

config["boltzmannSolver"]["collisions"]   = lxcat_path
config["boltzmannSolver"]["solver_type"]  = args.solver_type
config["boltzmannSolver"]["output_fname"] = args.out_fname
config["boltzmannSolver"]["threads"]      = str(4)
config["gpu"]["numGpusPerRank"]           = str(args.ngpus_per_node)

for i in range(len(sub_clusters)):
    config["boltzmannSolver"]["n_sub_clusters"] = str(sub_clusters[i])
    with open (output_folder+"/plasma.6sp.tps2boltzmann_ss_%d.ini"%(node_count[i]),"w") as f:
        config.write(f)
        f.close()
        

        
        
    
