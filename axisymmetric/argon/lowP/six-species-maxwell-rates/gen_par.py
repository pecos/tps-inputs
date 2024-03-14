import configparser
output_folder = "par_ss/ls6"
base_file     = "plasma.6sp.tps2boltzmann.ini"
lxcat_path    = "/scratch/03727/tg830270/tps_apptainer/tps/boltzmann/BESolver/python/lxcat_data/eAr_crs.6sp_Tg_0.5eV" 
sub_clusters  = [2048, 1024, 512, 256, 128]

config = configparser.ConfigParser()
config.read(base_file)
config["boltzmannSolver"]["collisions"]=lxcat_path
for i in range(len(sub_clusters)):
    config["boltzmannSolver"]["n_sub_clusters"] = str(sub_clusters[i])
    with open (output_folder+"/plasma.6sp.tps2boltzmann_%d.ini"%(i),"w") as f:
        config.write(f)
        f.close()
        

        
        
    