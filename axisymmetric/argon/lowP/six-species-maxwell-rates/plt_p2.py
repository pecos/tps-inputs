import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


folder_name = "tps_bte_x1_Nc_Conv"
Ncs         = [64, 128, 256, 512]
rel_errors      = list()
rel_errors_l2   = list()
rel_errors_loo  = list()

vgrids      = [3]

for grid_idx in vgrids:
    
    tps_fields = np.genfromtxt("%s/tps_fetch_grid_%02d_rank_00_npes_01.csv"%(folder_name, grid_idx), delimiter=",", skip_header=True)
    #     0,    1,  2 ,     3 ,       4,          5,          6,          7,  8
    # Ex   ,   Ey, Tg , ne/n0 , (Ar)/n0,(Ar*(1))/n0,(Ar*(2))/n0,(Ar*(3))/n0, n0
    
    n0     = tps_fields[:,8]
    Ex     = (tps_fields[:,0]/n0/1e-21) * 3.22e22 * 1e-21 
    Ey     = (tps_fields[:,1]/n0/1e-21) * 3.22e22 * 1e-21
    E      = np.sqrt(Ex**2 + Ey**2)
    
    data = [np.genfromtxt("%s/ts_Nc%d_grid_%02d_rank_0_npes_1_qoi.csv"%(folder_name, Nc, grid_idx), delimiter=",", skip_header=True) for Nc in Ncs]
    data.append(np.genfromtxt("%s/ts_all_grid_%02d_rank_0_npes_1_qoi.csv"%(folder_name, grid_idx), delimiter=",", skip_header=True))
    
    
    print("Ex -- %.8E"%(np.linalg.norm(data[-1][:,7] - Ex)))
    print("Ey -- %.8E"%(np.linalg.norm(data[-1][:,8] - Ey)))
    print("E  -- %.8E"%(np.linalg.norm(data[-1][:,9] - E)))
    
    N = n0.reshape(-1, 1) * np.concatenate([tps_fields[:, 4].reshape(-1,1), 
                        tps_fields[:, 5].reshape(-1,1), # excitation 0
                        tps_fields[:, 6].reshape(-1,1), # excitation 1
                        tps_fields[:, 7].reshape(-1,1), # excitation 3
                        tps_fields[:, 4].reshape(-1,1), # ionization 
                        tps_fields[:, 5].reshape(-1,1), # step-ionization 0
                        tps_fields[:, 6].reshape(-1,1), # step-ionization 1
                        tps_fields[:, 7].reshape(-1,1), # step-ionization 2
                        ], axis=1)
    
    def normalize(obs, xp):
        std_obs   = xp.std(obs, axis=0)
        std_obs[std_obs == 0.0] = 1.0
        return obs/std_obs, std_obs
    
    def inp_data(x, xi, di):
        xp          = np
        
        xn, xn_std  = normalize(x, xp)
        xin         = xi/xn_std
        
        distance    = xp.linalg.norm(xn[:, None, :] - xin[None, :, :], axis=2)
        pred        = xp.argmin(distance, axis=1)
        
        Nc          = len(xi)
        idx         = np.arange(Nc)
        mask        = pred == idx[:, None]
        
        d           = np.zeros((len(x), di.shape[1]))
        
        for c_idx in range(Nc):
            inp_idx      = mask[c_idx]
            d[inp_idx,:] = di[c_idx][:]
        
        return d
    
    tmp     = list()
    
    tmp_l2  = list()
    tmp_loo = list()

    idx_coord  = range(0,9) 
    idx_qoi    = range(13, data[-1].shape[1])
    print("data all \n", data[-1][:,idx_qoi] * N)
    Tg_all     = tps_fields[:, 2]
    idx_filter = Tg_all > 0 #np.logical_and(Tg_all>6000, Tg_all<7300)
    #print(Tg_all, Tg_all[idx_filter])
    for i in range(len(data)-2):
        dinp       = inp_data(data[-1][idx_filter,:][:,idx_coord] , data[i][:,idx_coord], data[i][:, idx_qoi])
        
        d1         = data[-1][idx_filter][:, idx_qoi] * N[idx_filter]
        d2         = dinp * N[idx_filter]
        
        ksns_inf   = np.max(np.abs(d1), axis=0)
        ksns_l2    = np.linalg.norm(np.abs(d1), axis=0)
            
        #rel_error  = np.linalg.norm(d2-d1) / np.linalg.norm(d1)  
        #rel_error  = np.abs(d1-d2) / np.max(np.abs(d1), axis=0) 
        rel_error   = np.abs(d1-d2) / ksns_l2
        # print(tps_fields[np.argmax(rel_error, axis=0),:])
        # rel_error   = np.max(rel_error, axis=0)
        #print(rel_error.shape)
        #print("tps \n", tps_fields[idx_filter, :][rel_error[:,2] > 1e-2 ,:])
        #print(rel_error[: , 0])
        tmp.append(rel_error)
        
        tmp_l2 .append(np.linalg.norm((d1-d2)/ ksns_l2,  ord=2    , axis=0))   
        tmp_loo.append(np.max(np.abs(d1-d2)  / ksns_inf, axis=0))  
        if i < len(Ncs):
            print("using %d\n" %(Ncs[i]), d2)
        else:
            print("using %s\n" %("all"), d2)
    
    rel_errors_loo.append(tmp_loo)    
    rel_errors_l2.append(tmp_l2)
    rel_errors.append(tmp)

col_names   = {1: r"$e$ + $Ar$    $\rightarrow$  $e + Ar_m$", 
               2: r"$e$ + $Ar$    $\rightarrow$  $e + Ar_r$",
               3: r"$e$ + $Ar$    $\rightarrow$  $e + Ar_p$",
               5: r"$e$ + $Ar_m$  $\rightarrow$  $e + Ar^+$",
               6: r"$e$ + $Ar_r$  $\rightarrow$  $e + Ar^+$",
               7: r"$e$ + $Ar_p$  $\rightarrow$  $e + Ar^+$",
               }

col_idx      = [1, 2, 3, 5, 6, 7]

# for idx in range(len(Ncs)):
#     data        = rel_errors[0][idx][:, col_idx].T
    
#     cc          = list()
#     for k,v in col_names.items():
#         cc.append(v)
        
#     sns.displot(data=pd.DataFrame({r"relative error": data.ravel(), "C":np.repeat(np.arange(data.shape[0]), data.shape[1])}), x=r"relative error", col="C", kde=True, height=3, log_scale=True)
#     #plt.grid(visible=True)
#     plt.tight_layout()
#     plt.savefig("output_%02d.png"%(idx))
#     plt.close()

dd0       = rel_errors[0][0][:, col_idx].T

dd1       = rel_errors[0][0][:, col_idx].T 
dd2       = rel_errors[0][1][:, col_idx].T 
dd3       = rel_errors[0][2][:, col_idx].T 
#dd4       = rel_errors[0][3][:, col_idx].T 

fig, axes = plt.subplots(2, 3, figsize=(8, 5), dpi=300)

for c_idx, c in enumerate(col_idx):
    plt.subplot(2, 3, c_idx + 1)
    sns.histplot(dd2[c_idx,:],  kde=True, log_scale=True)
    # sns.kdeplot(dd1[c_idx,:],  log_scale=True, label=r"$N_c=64$", gridsize=1000)
    # sns.kdeplot(dd2[c_idx,:],  log_scale=True, label=r"$N_c=128$", gridsize=1000)
    # sns.kdeplot(dd3[c_idx,:],  log_scale=True, label=r"$N_c=256$", gridsize=1000)
    #sns.kdeplot(dd4[c_idx,:],  log_scale=True, label=r"$N_c=512$")
    #plt.xlabel(r"relative error ")
    #plt.ylabel(r"density")
    #plt.legend()
    plt.ylabel(r"# of occurances")
    plt.title(col_names[c])
    plt.grid(visible=True)
    
plt.tight_layout()
plt.savefig("output.png")

print("rel l2")
for i in range(len(data)-2):
    print("Nc=%03d "%(Ncs[i]), end="")
    print(rel_errors_l2[0][i][col_idx])

print("rel linf")
for i in range(len(data)-2):
    print("Nc=%03d "%(Ncs[i]), end="")
    print(rel_errors_loo[0][i][col_idx])
    