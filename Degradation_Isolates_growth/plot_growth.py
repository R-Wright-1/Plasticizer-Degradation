import csv
import numpy
import matplotlib.pyplot as plt

days = ['Day 1.csv', 'Day 2.csv', 'Day 4.csv', 'Day 7.csv', 'Day 14.csv']
days = ['Day 1.csv', 'Day 2.csv', 'Day 4.csv', 'Day 7.csv']
days_TPA = ['Day 1 TPA.csv', 'Day 2 TPA.csv', 'Day 4 TPA.csv', 'Day 7 TPA.csv', 'Day 14 TPA.csv']
x = [0, 1, 2, 4, 7]

def get_file(fn):
    with open(fn, 'rU') as f:
        rows = []
        for row in csv.reader(f):
            rows.append(row)
    ha = rows[23][2:-1]+rows[24][2:-1]+rows[25][2:5]
    my = rows[25][5:-1]+rows[26][2:-1]+rows[27][2:8]
    bl = rows[27][8:-1]+rows[28][2:-1]+rows[29][2:-1]
    mean_bl, this_bl = [], []
    for a in range(len(bl)):
        this_bl.append(float(bl[a]))
        if (a+1) %3 == 0:
            mean_bl.append(numpy.mean(this_bl))
            this_bl = []
    new_ha, new_my = [], []
    this_ha, this_my = [], []
    print(len(mean_bl))
    for b in range(len(ha)):
        this_ha.append(float(ha[b]))
        this_my.append(float(my[b]))
        if (b+1) % 3 == 0:
            new_ha.append(this_ha)
            new_my.append(this_my)
            this_ha, this_my = [], []
    ha, my = new_ha, new_my
    """
    for c in range(len(ha)):
        for d in range(len(ha[c])):
            if c == 0:
                ha[c][d] -= mean_bl[c]
                my[c][d] -= mean_bl[c+1]
            else:
                ha[c][d] -= mean_bl[c+1]
                my[c][d] -= mean_bl[c+1]
    """
    return ha, my

def get_plot(days, x, savename):
    halo, myco = [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []]
    plt.figure(figsize=(10, 6))
    for a in range(len(days)):
        ha, my = get_file(days[a])
        for b in range(len(ha)):
            halo[b].append(ha[b])
            myco[b].append(my[b])
    ax1 = plt.subplot(241)
    ax3, ax2, ax4, ax5, ax6, ax7, ax8, ax9 = plt.subplot(242, sharex=ax1, sharey=ax1), plt.subplot(242, sharex=ax1, sharey=ax1), plt.subplot(243, sharex=ax1, sharey=ax1), plt.subplot(244, sharex=ax1, sharey=ax1), plt.subplot(245, sharex=ax1, sharey=ax1), plt.subplot(246, sharex=ax1, sharey=ax1), plt.subplot(247, sharex=ax1, sharey=ax1), plt.subplot(248, sharex=ax1, sharey=ax1)
    axis = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]
    labels = ['Labile substrate', 'Phthalic acid', 'BHET', 'DBP', 'DEHP', 'DINP', 'DIDP', 'ATBC', 'TOTM']
    ls = [r'$Halomonas$'+'\nsp. ATBC28', r'$Mycobacterium$'+'\nsp. DBP42']
    rmy = [ax2, ax4, ax5, ax7, ax8, ax9]
    for y in rmy:
        plt.sca(y)
        plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)

    for a in range(len(halo)):
        if a == 2:
            continue
        this_mean_ha, this_std_ha = [], []
        this_mean_my, this_std_my = [], []
        for b in range(len(halo[a])):
            this_mean_ha.append(numpy.mean(halo[a][b]))
            this_std_ha.append(numpy.std(halo[a][b]))
            this_mean_my.append(numpy.mean(myco[a][b]))
            this_std_my.append(numpy.std(myco[a][b]))
        axis[a].set_xlim([x[0]-0.5, x[-1]+0.5])
        add0, addsd = 0.04, 0
        if a == 2:
            add0 = 0.09
        axis[a].plot(x, [add0]+this_mean_ha, color='b', marker='o', linestyle='-', label=ls[0], markeredgecolor='k')
        axis[a].plot(x, [add0]+this_mean_my, color='g', marker='^', linestyle='-.', label=ls[1], markeredgecolor='k')
        
        axis[a].errorbar(x, [add0]+this_mean_ha, yerr=[addsd]+this_std_ha, color='b', marker='o', linestyle='-', capsize=3, markeredgecolor='k')
        axis[a].errorbar(x, [add0]+this_mean_my, yerr=[addsd]+this_std_my, color='g', marker='^', linestyle='-.', capsize=3, markeredgecolor='k')
        axis[a].set_title(labels[a])
        plt.setp(axis[a], xticks=[0,1,2,4,7])
    axis[0].set_ylabel('Absorbance (600 nm)')
    axis[5].set_ylabel('Absorbance (600 nm)')
    axis[5].set_xlabel('Days'), axis[6].set_xlabel('Days'), axis[7].set_xlabel('Days'), axis[8].set_xlabel('Days')
    axis[4].legend(loc='upper left', bbox_to_anchor=(1,1.05))
    axis[2].set_ylim([0.02, 0.18])
    plt.tight_layout()
    plt.savefig('Growth day '+str(x[-1])+savename+'.png', dpi=600, bbox_inches='tight')
    return
get_plot(days, x, '')