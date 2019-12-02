import csv
import numpy
import matplotlib.pyplot as plt

#Give csv names, x values and colors for each bacterium
days = ['Day 1.csv', 'Day 2.csv', 'Day 4.csv', 'Day 7.csv']
x = [0, 1, 2, 4, 7]
Hcol, Mcol = '#F4B183', '#9DC3E6'

#Function to read in the excel file (output by plate reader) and get means for each triplicate
def get_file(fn):
    #Read in csv file
    with open(fn, 'rU') as f:
        rows = []
        for row in csv.reader(f):
            rows.append(row)
    #Get all readings for each bacterium (ha and my)
    ha = rows[23][2:-1]+rows[24][2:-1]+rows[25][2:5]
    my = rows[25][5:-1]+rows[26][2:-1]+rows[27][2:8]
    new_ha, new_my = [], []
    this_ha, this_my = [], []
    #Get means of triplicates
    for b in range(len(ha)):
        this_ha.append(float(ha[b]))
        this_my.append(float(my[b]))
        if (b+1) % 3 == 0:
            new_ha.append(this_ha)
            new_my.append(this_my)
            this_ha, this_my = [], []
    ha, my = new_ha, new_my
    return ha, my

def get_plot(days, x):
    #Call the above function for each of the measurement days, and separate these into measurements for each substrate
    halo, myco = [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []]
    for a in range(len(days)):
        ha, my = get_file(days[a])
        for b in range(len(ha)):
            halo[b].append(ha[b])
            myco[b].append(my[b])
    #Set up figure, axis and labels
    plt.figure(figsize=(10, 6))
    ax1 = plt.subplot(241)
    ax3, ax2, ax4, ax5, ax6, ax7, ax8, ax9 = plt.subplot(242, sharex=ax1, sharey=ax1), plt.subplot(242, sharex=ax1, sharey=ax1), plt.subplot(243, sharex=ax1, sharey=ax1), plt.subplot(244, sharex=ax1, sharey=ax1), plt.subplot(245, sharex=ax1, sharey=ax1), plt.subplot(246, sharex=ax1, sharey=ax1), plt.subplot(247, sharex=ax1, sharey=ax1), plt.subplot(248, sharex=ax1, sharey=ax1)
    axis = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]
    labels = ['Labile substrate', 'Phthalic acid', 'BHET', 'DBP', 'DEHP', 'DINP', 'DIDP', 'ATBC', 'TOTM']
    ls = [r'$Halomonas$'+'\nsp. ATBC28', r'$Mycobacterium$'+'\nsp. DBP42']
    rmy = [ax2, ax4, ax5, ax7, ax8, ax9]
    for y in rmy:
        plt.sca(y)
        plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)
    #Plot the measurements for each treatment into the right axis, skipping this is the measurements are for BHET, which wasn't included in the end manuscript
    for a in range(len(halo)):
        if a == 2:
            continue
        #Get means and standard deviations of triplicates
        this_mean_ha, this_std_ha = [], []
        this_mean_my, this_std_my = [], []
        for b in range(len(halo[a])):
            this_mean_ha.append(numpy.mean(halo[a][b]))
            this_std_ha.append(numpy.std(halo[a][b]))
            this_mean_my.append(numpy.mean(myco[a][b]))
            this_std_my.append(numpy.std(myco[a][b]))
        axis[a].set_xlim([x[0]-0.5, x[-1]+0.5])
        #add0 is the measurements taken on day 0 that are not included in these excel sheets
        add0, addsd = 0.04, 0
        #Plot with no errorbars with labels - for the legend, so that errorbars are not present in the legend
        axis[a].plot(x, [add0]+this_mean_my, color=Mcol, marker='^', linestyle='-', label=ls[1], markeredgecolor='k')
        axis[a].plot(x, [add0]+this_mean_ha, color=Hcol, marker='o', linestyle='-.', label=ls[0], markeredgecolor='k')
        
        #Now plot the same thing again, but with errorbars
        axis[a].errorbar(x, [add0]+this_mean_my, yerr=[addsd]+this_std_my, color=Mcol, marker='^', linestyle='-', capsize=3, markeredgecolor='k')
        axis[a].errorbar(x, [add0]+this_mean_ha, yerr=[addsd]+this_std_ha, color=Hcol, marker='o', linestyle='-.', capsize=3, markeredgecolor='k')
        
        #These are the values taken for "plot_growth_consumption.py"
        print(a), print(labels[a])
        print('Halo growth', [add0]+this_mean_ha)
        print('Myco growth', [add0]+this_mean_my)
        print('Halo error', [addsd]+this_std_ha)
        print('Myco error', [addsd]+this_std_my)
        
        #Add correct title and change x tick frequncy to only be on days measurements were taken
        axis[a].set_title(labels[a])
        plt.setp(axis[a], xticks=[0,1,2,4,7])
    #Add axis labels and save figure
    axis[0].set_ylabel('Absorbance (600 nm)')
    axis[5].set_ylabel('Absorbance (600 nm)')
    axis[5].set_xlabel('Days'), axis[6].set_xlabel('Days'), axis[7].set_xlabel('Days'), axis[8].set_xlabel('Days')
    axis[4].legend(loc='upper left', bbox_to_anchor=(1,1.05))
    axis[2].set_ylim([0.02, 0.18])
    plt.tight_layout()
    plt.savefig('Growth day '+str(x[-1])+'.png', dpi=600, bbox_inches='tight')
    return
get_plot(days, x)