import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np
import os

fns = ['Gene_cluster_Mhous_phthalate.csv', 'Gene_cluster_Mhous_fatty_acid_long.csv', 'Gene_cluster_Mhous_fatty_acid_short.csv', 'Gene_cluster_Hcamp_phthalate.csv', 'Gene_cluster_Hcamp_fatty_acid_long.csv', 'Gene_cluster_Hcamp_fatty_acid_short.csv']

def get_file_details(fn):
    #Gene	Name	Enzyme	Bp	F/C	PA	DBP	DEHP	ATBC
    with open(fn, 'rU') as f:
        rows = []
        for row in csv.reader(f):
            rows.append(row)
    del rows[0]
    for a in range(len(rows)):
        for b in range(len(rows[a])):
            if b == 1:
                if len(rows[a][b]) == 3:
                    rows[a][b] = '0'+rows[a][b]
            elif b == 3:
                if rows[a][b] == '':
                    rows[a][b] = 200
                rows[a][b] = float(rows[a][b])
            elif b > 4:
                rows[a][b] = float(rows[a][b])
    return rows

def remove_axis(ax):
    ax.tick_params(axis='x',which='both',top='off', bottom='off')
    plt.setp(ax.get_xticklabels(), visible=False)
    ax.tick_params(axis='y',which='both',left='off', right='off')
    plt.setp(ax.get_yticklabels(), visible=False)
    return

def get_box(mid, row, ax):
    cmap_up = 'seismic'
    norm_up = mpl.colors.Normalize(vmin=-8, vmax=10)
    colormap_up = mpl.cm.get_cmap(cmap_up, 256)
    m_up = mpl.cm.ScalarMappable(norm=norm_up, cmap=colormap_up)

    cmap_down = 'seismic'
    norm_down = mpl.colors.Normalize(vmin=-10, vmax=8)
    colormap_down = mpl.cm.get_cmap(cmap_down, 256)
    m_down = mpl.cm.ScalarMappable(norm=norm_down, cmap=colormap_down)
    
    fold = row[-4:]
    fold_colors = []
    text_colors = []
    y = 150
    x = [mid-(2*y), mid-y, mid, mid+y]
    plt.sca(ax)
    trt = ['PA', 'DBP', 'DEHP', 'ATBC']
    for b in range(len(fold)):
        if fold[b] == 0:
            fold_colors.append('k')
        else:
            if fold[b] < 1 and fold[b] != 0:
                fold[b] = -(1/fold[b])
            if fold[b] > 0:
                fold_colors.append(m_up.to_rgba(fold[b]))
            elif fold[b] < 0:
                fold_colors.append(m_down.to_rgba(fold[b]))
            else:
                fold_colors.append('w')
        if fold[b] > 7.5 or fold[b] < -5:
            text_colors.append('w')
        elif fold[b] == 0:
            text_colors.append('w')
        else:
            text_colors.append('k')
        y1, y2, y3 = 1.15, 1.85, 1.45
        if fold[b] != 0:
            if ax == ax1 and row[1] == '3198' or row[1] == '3200': y1, y2, y3 = 2.5, 3.2, 2.8
            rectangle = mpatches.Rectangle((x[b], y1), y, 0.6, angle=0.0, edgecolor='k', facecolor=fold_colors[b])
            ax.add_patch(rectangle)
            ax.text(x[b]+75, y2, trt[b], va='bottom', ha='center', fontsize=40, rotation=90)
            if fold[b] != 0:
                ax.text(x[b]+75, y3, str(int(fold[b])), ha='center', va='center', fontsize=30, color=text_colors[b])
    return

def plot_arrow(rows, ax, color, enzyme_name):
    fs = 50
    start, length = [], []
    count = 10
    for a in range(len(rows)):
        start.append(count)
        length.append(rows[a][3])
        count += rows[a][3]+10
    arrowstyle = mpatches.ArrowStyle.Simple(head_width=150,tail_width=80,head_length=50)
    ax.plot([-400, start[0]], [0,0], 'k--')
    ax.plot([start[-1]+length[-1], start[-1]+length[-1]+200], [0,0], 'k--')
    mids = []
    for a in range(len(start)):
        if rows[a][4] == 'F':
            arrow = mpatches.FancyArrowPatch((start[a], 0), (start[a]+length[a], 0), arrowstyle=arrowstyle, facecolor=color[a])
        else:
            arrow = mpatches.FancyArrowPatch((start[a]+length[a], 0), (start[a], 0), arrowstyle=arrowstyle, facecolor=color[a])
        midpoint = (length[a]/2)+start[a]
        mids.append(midpoint)
        ax.add_patch(arrow)
        ax.text(midpoint-150, -0.5, enzyme_name[a], rotation=45, horizontalalignment='center', verticalalignment='top', fontsize=fs)
        ax.text(midpoint, 0.8, rows[a][1], horizontalalignment='center', verticalalignment='center', fontsize=fs+10, color='k')
        get_box(midpoint, rows[a], ax)
    remove_axis(ax)
    return

fig = plt.figure(figsize=(100,100))
ax1 = plt.subplot2grid((7,1), (0,0), frameon=False)
ax1.set_ylim([-1.5, 3.5])
ax1.set_xlim([-200, 13299])
ax2 = plt.subplot2grid((7,1), (1,0), sharex=ax1, sharey=ax1, frameon=False)
ax3 = plt.subplot2grid((7,1), (2,0), sharex=ax1, sharey=ax1, frameon=False)
ax4 = plt.subplot2grid((14,1), (7,0), sharex=ax1, sharey=ax1, frameon=False, rowspan=2)
ax5 = plt.subplot2grid((14,1), (9,0), sharex=ax1, sharey=ax1, frameon=False, rowspan=2)
ax6 = plt.subplot2grid((14,1), (11,0), sharex=ax1, sharey=ax1, frameon=False, rowspan=2)

colors = [['#800080', '#800080', '#800080', '#800080', '#800080', '#800080', '#800080', '#800080', 'k', '#800080', '#800080', '#800080', '#800080', '#800080', '#800080'], 
           ['k', '#800080', 'k', '#800080', '#800080', 'k', '#800080'], 
           ['#800080', '#800080', '#800080', '#800080', '#800080', '#800080'], 
           ['k', 'k', 'r', 'k', '#800080', 'k', 'k', 'k', 'k', '#800080', '#800080'], 
           ['#800080', '#800080', '#800080', '#800080'], 
           ['#800080', '#800080', '#800080', '#800080', '#800080', '#800080', 'k', 'k', 'k', '#800080', 'k', 'k', '#800080']]

enzyme_names = [['3,4-dihydroxy\nphthalate\ndecarboxylase', 'Rhodocoxin\nreductase', 'Ferredoxin', 'Cis-toluene\ndihydrodiol\ndehydrogenase', 'Hypothetical\nprotein', 'Phthalate\n3,4-dioxygenase', 'Phthalate\n3,4-dioxygenase', 'Transcriptional\nregulator', 'Transcriptional\nregulator', 'Protocatechuate\n3,4-dioxygenase',  'Protocatechuate\n3,4-dioxygenase', '3-carboxy-\n'+'$cis,cis$-muconate'+'\ncycloisomerase', '3-oxoadipate\nenol-lactonase', '3-oxoadipate\nCoA-transferase', '3-oxoadipate\nCoA-transferase'], 
                ['Aldehyde\ndehydrogenase', 'Alcohol\ndehydrogenase', 'Fatty acid\nCoA dehydrogenase', '2,3-dehydroadipyl\nCoA dehydrogenase', 'Fatty acid\nCoA ligase', 'Acetyl-CoA\naxyltransferase', 'CoA transferase'], 
                ['Alcohol\ndehydrogenase', 'Acyl-CoA\ndehydrogenase', 'Enoyl-CoA\nhydratase', 'Enoyl-CoA\nhydratase/isomerase', 'Acyl-CoA\ndehydrogenase', 'Acyl-CoA\ndehydrogenase'], 
                ['Phthalate\n4,5-dioxygenase', 'Phthalate\n4,5-dioxygenase', 'Solute-binding\nprotein', 'Protocatechuate\n3,4-dioxygenase\nalpha subunit', 'Protocatechuate\n3,4-dioxygenase\nbeta subunit', 'Transcriptional\nregulator', '3-oxoadipate\nenol-lactonase', '\u03B2-ketoadipyl-CoA'+'\nthiolase', '3-oxoadipate\nCoA-transferase\nsubunit B', '3-oxoadipate\nCoA-transferase\nsubunit A', '3-carboxy-\n'+'$cis,cis$-muconate'+'\ncycloisomerase'],
                ['Acyl-CoA\ndehydrogenase', 'Fatty acid\nCoA ligase', 'Acyl-CoA\ndehydrogenase', 'Enoyl-CoA\nhydratase'],
                ['Fatty acyl-CoA\nsynthase', 'Hydroxymethyl\nglutaryl-CoA\nlyase', 'Acetyl-CoA\ncarboxylase', 'Enoyl-CoA\nhydratase', 'Acetyl-CoA\ncarboxylase', 'Acyl-CoA\ndehydrogenase']]

axs = [ax1, ax2, ax3, ax4, ax5, ax6]

for a in range(len(fns)):
    fn, ax = fns[a], axs[a]
    rows = get_file_details(fn)
    plot_arrow(rows, ax, colors[a], enzyme_names[a])

fs = 80
fig.text(0.1, 0.99, 'Space', ha='left', va='center', fontsize=fs+30, color='w')
fig.text(0.1,0.91, '$Mycobacterium$ sp. DBP42', ha='left', va='center', fontsize=fs+30, color='w', bbox={'facecolor':'k', 'alpha':0.6, 'pad':40})
fig.text(0.1,0.5, '$Halomonas$ sp. ATBC28', ha='left', va='center', fontsize=fs+30, color='w', bbox={'facecolor':'k', 'alpha':0.6, 'pad':40})

ax1.text(-199, 0, 'Phthalate\ndegradation', va='center', ha='right', fontsize=fs)
ax2.text(-199, 0, 'Long chain\nfatty acid\n'+'\u03B2-oxidation', va='center', ha='right', fontsize=fs)
ax3.text(-199, 0, 'Short chain\nfatty acid\n'+'\u03B2-oxidation', va='center', ha='right', fontsize=fs)

ax4.text(-199, 0, 'Phthalate\ndegradation', va='center', ha='right', fontsize=fs)
ax5.text(-199, 0, 'Fatty acid\n'+'\u03B2-oxidation', va='center', ha='right', fontsize=fs)
ax6.text(-199, 0, 'Fatty acid\n'+'\u03B2-oxidation', va='center', ha='right', fontsize=fs)


os.chdir('/Users/robynwright/Documents/GitHub/PlasticizerDegradation/clusters_plots/original/')
plt.subplots_adjust(hspace=0.4)
plt.savefig('Clusters.png', bbox_inches='tight', dpi=600)
plt.close()