#!/bin/python3
import configparser

output_folder = "./"
base_file     = "plasma.6sp.tps2boltzmann.ini"
lxcat_path    = "/scratch/03727/tg830270/tps-bte/tps/boltzmann/BESolver/python/lxcat_data/eAr_crs.6sp_Tg_0.5eV" 
sub_clusters  = [1024, 512, 256, 128, 64]
node_count    = [1, 2, 4, 8, 16]

config = configparser.ConfigParser()
config.optionxform=str
config.read(base_file)

config["boltzmannSolver"]["collisions"]   = lxcat_path
config["boltzmannSolver"]["solver_type"]  = "steady-state"
config["boltzmannSolver"]["output_fname"] = "bte_ss"
config["gpu"]["numGpusPerRank"]           = str(3)

for i in range(len(sub_clusters)):
    config["boltzmannSolver"]["n_sub_clusters"] = str(sub_clusters[i])
    with open (output_folder+"/plasma.6sp.tps2boltzmann_ss_%d.ini"%(node_count[i]),"w") as f:
        config.write(f)
        f.close()
        

        
        
    
