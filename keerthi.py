'''
O4: /global/cfs/cdirs/m4237/keerthi/gw_sim/Farah_latest/observing-scenarios-simulations/runs/O4/coincs_O4.xml
O5: /global/cfs/cdirs/m4237/keerthi/gw_sim/Farah_latest/observing-scenarios-simulations/runs/O5/coincs_O5.xml
O4_stats_BBH: /global/cfs/cdirs/m4237/keerthi/gw_sim/Farah_latest/observing-scenarios-simulations/runs/O4/stats_O4bbh.tsv
O5_stats_BBH: /global/cfs/cdirs/m4237/keerthi/gw_sim/Farah_latest/observing-scenarios-simulations/runs/O5/stats_O5bbh.tsv
O4_bbh_skymaps: /global/cfs/cdirs/m4237/keerthi/gw_sim/Farah_latest/observing-scenarios-simulations/runs/O4/bbh_fits
O5_bbh_skymaps: /global/cfs/cdirs/m4237/keerthi/gw_sim/Farah_latest/observing-scenarios-simulations/runs/O5/bbh_fits
'''

table1 = Table.read(path_coinc_O4, tablename='sim_inspiral')
table1_ = Table.read(path_coinc_O4, tablename='sngl_inspiral')
table1__ = Table.read(path_coinc_O4, tablename='coinc_inspiral')
# Apply masks
mask1 = (table1['inclination'] > 0)
t1 = table1[mask1]

mask1_ = (table1_['mass1'] > 0)
t1_ = table1_[mask1_]

mask1__ = (table1__['mass'] > 0)
t1__ = table1__[mask1__]





#combine tables

from astropy.table import join
# Rename 'coinc_event_id' to 'simulation_id' in t1__
t1__ = t1__.copy()
t1__['simulation_id'] = t1__['coinc_event_id']
t1__['net_snr'] = t1__['snr']
del t1__['coinc_event_id'],t1__['snr']
# Merge t1 and t1_ based on mass1
merged_t1_t1_ = join(t1, t1_, keys='mass1', join_type='inner')
# Merge the merged_t1_t1_ with t1__ based on simulation_id
merged_t1_final = join(merged_t1_t1_, t1__, keys='simulation_id', join_type='inner')
import numpy as np
# Select specified columns from merged_t1_final
selected_columns = ['coa_phase_1', 'distance', 'inclination', 'latitude', 'longitude',
                    'mass1', 'polarization', 'simulation_id', 'mass2_1', 'spin1z_1',
                    'spin2z_1', 'ifos', 'snr', 'net_snr']
t1_f = merged_t1_final[selected_columns]

import pandas as pd

# Convert the Astropy table to a Pandas DataFrame
t1_df = t1_f.to_pandas()

# Drop duplicate rows based on mass1 and mass2_1
t1_df = t1_df.drop_duplicates(subset=['mass1', 'mass2_1'])

t1_df.to_csv('/global/cfs/cdirs/m4237/keerthi/gw_sim/Farah_latest/observing-scenarios-simulations/runs/O4_noV_snrcut/coinc_O4noV.dat',index=False,sep="\t")





#Matching combined table with the stats file

idx_bns = (tc["mass1"] > 3.0) & (tc["mass2"] > 3.0)
Mass1 = tc["mass1"][idx_bns]
Mass2 = tc["mass2"][idx_bns]
SNR = tc["snr"][idx_bns]
SNR_net = tc["net_snr"][idx_bns]
id = tc["simulation_id"][idx_bns]

Area_50_bns = []
Area_70_bns = []
Area_90_bns = []
for i in range(len(id)):
    idx_bns_match = np.where(df1["coinc_event_id"]==(id[i]))
    if idx_bns_match[0].shape[0] > 0:

        Area_50_bns.append(df1["area50"][idx_bns_match[0]])
        Area_70_bns.append(df1["area70"][idx_bns_match[0]])
        Area_90_bns.append(df1["area90"][idx_bns_match[0]])