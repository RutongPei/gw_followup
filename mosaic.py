from astropy.table import QTable
from astropy import units as u
import numpy as np
from gwpy import table as table
import pandas as pd
import matplotlib.pyplot as plt

# convert to latex
def dl (unit=True):
    if (unit == False):
        return r'$d_L$'
    return r'$d_L$ [Mpc]'

def log_n_agn():
    return r'log$_{10}$ N$_{AGN}$'

def mtotal(unit=True):
    if (unit == False):
        return r'm$_{total}$ '
    return r'm$_{total}$ ' + r'[M$_{\odot}]$'

def area(a, unit=True):
    s = str(a)
    if (unit == False):
        return 'area (' + s + r'$\%$ CL)'
    return 'area (' + s + r'$\%$ CL)' + r'[deg$^{2}$]'



def get_O5(file_path):
    df = pd.read_csv(file_path, sep='\t')


    m1 = df['mass1']
    m2 = df['mass2']
    m_total = m1 + m2

    area50 = df['Area50']
    area70 = df['Area70']
    area90 = df['Area90']

    vol50 = df['Vol50']
    vol70 = df['Vol70']
    vol90 = df['Vol90']

    dis70 = df['Dis70']
    dis50 = df['Dis50']

    dis = df['distance']

    # agn density = 10^-4.75 agn/volume 
    # note: vol has units Mpc3
    agn_count = [v * 10 ** (-4.75) for v in vol90]

    # agn flare density = 10^-4 flare/agn
    agn_flare = [c * 10 ** (-4) for c in agn_count]

    return m_total, area70, dis, agn_count, agn_flare


#TODO: take in fits file?
def plot_mosaic(mass, distance, area, volume):
    # get event info (O5, sim_id = 2)
    flare = volume * 10 ** (-4) * 10 ** (-4.75)
    mass = 27.17 + 25.92
    distance = 1364.50

    # get O5
    file_path = "/global/homes/r/rutong/gw_followup/list_O5bbh.dat"
    m_total, area70, dis, agn_count, agn_flare = get_O5(file_path)
    # Create the mosaic layout
    layout = [
        ["A", "B"],
        ["C", "."]
    ]

    fig, axes = plt.subplot_mosaic(layout, figsize=(12, 10))

    # m_total vs. d_l (color by N_AGN)
    sc = axes['A'].scatter(dis, m_total, c=np.log10(agn_count), cmap='viridis', s=3)
    axes['A'].scatter (distance, mass, s=15, color='red')
    axes['A'].set_title(mtotal(unit=False) + ' vs. ' + dl(unit=False))
    axes['A'].set_xlabel(dl())
    axes['A'].set_ylabel(mtotal())
    axes['A'].set_xscale('log')
    axes['A'].set_yscale('log')
    cbar = fig.colorbar(sc, ax=axes['A'])
    cbar.set_label(log_n_agn())

    # AGN flares CDF
    bin = np.logspace(-2, 2.2, 30)
    axes['B'].hist(agn_flare, bins=bin, edgecolor='black', cumulative=True, density=True, histtype='step')
    axes['B'].axvline(flare, color='red', linestyle='dotted', linewidth=2)
    axes['B'].set_title('AGN Flares CDF')
    axes['B'].set_xlabel('AGN flare')
    axes['B'].set_ylabel('CDF')
    axes['B'].set_xscale('log')

    # 70% area vs. d_l (color by N_AGN)
    sc2 = axes['C'].scatter(dis, area70, c=np.log10(agn_count), cmap='plasma', s=3)
    axes['C'].set_title(area(70, unit=False) + ' vs. ' + dl(unit=False))
    axes['C'].set_xlabel(dl())
    axes['C'].set_ylabel(area(70))
    axes['C'].set_xscale('log')
    axes['C'].set_yscale('log')
    cbar2 = fig.colorbar(sc2, ax=axes['C'])
    cbar2.set_label(log_n_agn())

    plt.tight_layout()
    plt.show()
    
