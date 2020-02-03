import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
from config import FARGO_DIR, FIGURE_DIR
import sim_params


def main(sim_group):

    if sim_group not in ['migration']:
        return
    print('  plotting.migration.planet_ecc_vs_e0')

    initial_eccs_with_acc, final_eccs_with_acc = [], []
    initial_eccs, final_eccs = [], []

    for sim_id in sorted(os.listdir(os.path.join(FARGO_DIR, sim_group))):
        if sim_id in ['.DS_Store']:
            continue

        # get initial eccentricity, initial mass and gas disk viscosity
        ecc_0 = sim_params.planets.initial_eccentricity(sim_group, sim_id)
        m_0 = sim_params.planets.initial_mass(sim_group, sim_id)
        α = sim_params.planets.gas_disk_viscosity(sim_group, sim_id)
        if not (m_0 == 1e-3 and α == 1e-2):
            continue
        # is accretion turned on?
        acc_on = True if sim_id.split('_')[-1] == 'acc' else False
        # get ecc after sim is finished
        nr_of_outfiles = sim_params.general.nr_of_outputs(
            sim_group, sim_id
        )
        ecc_final = sim_params.planets.current_eccentricity(
            sim_group, sim_id, nr_of_outfiles
        )

        if acc_on:
            initial_eccs_with_acc.append(ecc_0)
            final_eccs_with_acc.append(ecc_final)
        else:
            initial_eccs.append(ecc_0)
            final_eccs.append(ecc_final)

    fig = plt.figure(figsize=(4, 3))
    plt.scatter(
        initial_eccs, final_eccs,
        label='without accretion', color='red'
    )
    plt.scatter(
        initial_eccs_with_acc, 2 * np.array(final_eccs_with_acc),
        label='with accretion', color='green'
    )
    plt.xlim(-0.025, max(initial_eccs_with_acc) + 0.025)
    #plt.ylim(0, 0.4)
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='x')
    plt.gca().ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    plt.legend(loc='upper left')
    plt.xlabel('initial planet eccentricity')
    plt.ylabel('final planet eccentricity')
    plt.gcf().subplots_adjust(left=0.2)
    plt.gcf().subplots_adjust(bottom=0.2)

    save_loc = os.path.join(
        FIGURE_DIR, sim_group, 'final_ecc_vs_initial_ecc.pdf'
    )
    plt.savefig(save_loc)
    plt.close()

