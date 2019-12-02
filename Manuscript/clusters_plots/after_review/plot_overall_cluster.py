import numpy
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib as mpl

plt.figure(figsize=(20,12))
#ax1 = plt.subplot(111)


fns = ['Gene_cluster_Mhous_phthalate.csv', 'Gene_cluster_Hcamp_benzoate.csv', 'Gene_cluster_Hcamp_benzoate2.csv', 'Gene_cluster_Hcamp_benzoate3.csv']

mhous = pd.read_csv(fns[0])
hcamp = pd.read_csv(fns[1])
hcamp2 = pd.read_csv(fns[2])
hcamp3 = pd.read_csv(fns[3])

ax1 = plt.subplot2grid((12,1), (0, 0), rowspan=3, frameon=False)
#ax1 = plt.subplot2grid((16, 1), (0, 0), frameon=False)
ax2 = plt.subplot(614, sharex=ax1, sharey=ax1, frameon=False)
ax3 = plt.subplot(615, sharex=ax1, sharey=ax1, frameon=False)
ax4 = plt.subplot(616, sharex=ax1, sharey=ax1, frameon=False)
#ax2 = plt.subplot2grid((16, 1), (6, 0), frameon=False, sharex=ax1, sharey=ax1, )
#ax3 = plt.subplot2grid((16, 1), (7, 0), frameon=False, sharex=ax1, sharey=ax1, )
#ax4 = plt.subplot2grid((16, 1), (8, 0), frameon=False, sharex=ax1, sharey=ax1, )
arrowstyle = mpatches.ArrowStyle.Simple(head_width=12,tail_width=8,head_length=4)
fs = 8

def get_box(mid, fold, ax, num):
    cmap_up = 'seismic'
    norm_up = mpl.colors.Normalize(vmin=-8, vmax=10)
    colormap_up = mpl.cm.get_cmap(cmap_up, 256)
    m_up = mpl.cm.ScalarMappable(norm=norm_up, cmap=colormap_up)

    cmap_down = 'seismic'
    norm_down = mpl.colors.Normalize(vmin=-10, vmax=8)
    colormap_down = mpl.cm.get_cmap(cmap_down, 256)
    m_down = mpl.cm.ScalarMappable(norm=norm_down, cmap=colormap_down)
    
    #fold = row[-4:]
    fold_colors = []
    text_colors = []
    y = 230
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
        y1, y2, y3 = -0.15, -0.16, -0.1
        if fold[b] != 0:
            if ax == ax1 and num == '3198' or num == '3200' or num == '3206' or num == '3209': y1, y2, y3 = -0.41, -0.42, -0.36
            rectangle = mpatches.Rectangle((x[b], y1), y, 0.1, angle=0.0, edgecolor='k', facecolor=fold_colors[b])
            ax.add_patch(rectangle)
            ax.text(x[b]+115, y2, trt[b], va='top', ha='center', fontsize=fs, rotation=90)
            if fold[b] != 0:
                ax.text(x[b]+115, y3, str(int(fold[b])), ha='center', va='center', fontsize=fs-1, color=text_colors[b])
    return

def plot_genes(ax, bac, adding):
    start = 0
    ax.plot([-400, start], [0, 0], 'k--', lw=1)
    for a in range(bac.shape[0]):
        if isinstance(bac.iloc[a, 0], str) == False:
            ax.plot([start, start+500], [0, 0], 'k--', lw=1)
            start += 500
            continue
        finish = start+bac.iloc[a, 3]
        if bac.iloc[a, 5] == 'Y': 
            color = 'r'
        elif bac.iloc[a, 5] == 'M':
            color = 'r'
        else:
            color = 'gray'
        if bac.iloc[a, 4] == 'F':
            arrow = mpatches.FancyArrowPatch((start, 0), (finish, 0), arrowstyle=arrowstyle, facecolor=color, shrinkA=0.2, shrinkB=0.1)
        else:
            arrow = mpatches.FancyArrowPatch((finish, 0), (start, 0), arrowstyle=arrowstyle, facecolor=color, shrinkA=0.2, shrinkB=0.1)
        mid = (finish-start)/2+start
        ax.add_patch(arrow)
        name = bac.iloc[a, 2]
        if name != '' and isinstance(name, str):
            for i in range(len(name)):
                if name[i] == ' ':
                    name = name[:i]+'\n'+name[i+1:]
                elif name[i] == '_':
                    name = name[:i]+' '+name[i+1:]
        elif isinstance(name, str) == False:
            name = ''
        if name == 'TRAP': 
            name = 'TRAP'
        elif name == 'Trans':
            name = 'Trans'
        elif name == 'ABC':
            name = 'ABC'
        elif name != '':
            name = '$'+name+'$'
        if adding == []:
            #ax.text(mid, -0.1,  name, horizontalalignment='center', verticalalignment='top', fontsize=fs)
            ax.text(mid, 0.05, str(int(bac.iloc[a, 1])).zfill(4)+'\n'+name, horizontalalignment='center', verticalalignment='bottom', fontsize=fs, color='k')
        else:
            #ax.text(mid, -0.1-adding[a], name, horizontalalignment='center', verticalalignment='top', fontsize=fs)
            ax.text(mid, 0.05+adding[a], str(int(bac.iloc[a, 1])).zfill(4)+'\n'+name, horizontalalignment='center', verticalalignment='bottom', fontsize=fs, color='k')
        if ax == ax1:
            get_box(mid, bac.iloc[a, -5:-1], ax1, str(int(bac.iloc[a, 1])).zfill(4))
        start = finish
    ax.set_ylim([-1, 1])
    plt.sca(ax)
    plt.axis('off')
    ax.plot([finish, finish+400], [0, 0], 'k--', lw=1)
    
    if ax == ax1:
        ax.set_ylim([-2, 1])
    return finish

fin1 = plot_genes(ax1, mhous, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] )
fin2 = plot_genes(ax2, hcamp, [])
fin3 = plot_genes(ax3, hcamp2, [])
fin4 = plot_genes(ax4, hcamp3, [])

fin = max(fin1, fin2, fin3, fin4)
ax1.set_xlim([-400, fin+400])
ax2.set_xlim([-400, fin+400])
ax3.set_xlim([-400, fin+400])
ax4.set_xlim([-400, fin+400])

ax1.text(-400, 0.3, '$Mycobacterium$ sp. DBP42', fontsize=fs+2)
ax2.text(-400, 0.2, '$Halomonas$ sp. ATBC28', fontsize=fs+2)


plt.subplots_adjust(hspace=-0.85)
plt.savefig('Clusters.png', dpi=600, bbox_inches='tight')