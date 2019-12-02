import matplotlib.pyplot as plt
import csv
import matplotlib as mpl
from matplotlib import rcParams
import math
import os

rcParams['axes.titlepad'] = 15
title1 = ''

fn = 'Hcamp'

#Change this to be the directory with 'Mhous_confirmed.csv' or 'Hcamp_confirmed.csv'
os.chdir('/Users/robynwright/Documents/GitHub/PlasticizerDegradation/supplementary_pathway_plots/'+fn+'/')

#Open the csv file - run twice for Halomonas with '_confirmed.csv' and '_confirmed_exo.csv' by setting exo to True or False
exo = True
if exo: ex, fc = '_exo', 'r'
else: ex, fc = '', 'k'
with open(fn+'_confirmed'+ex+'.csv', 'rU') as f:
    rows = []
    for row in csv.reader(f):
        rows.append(row)

#Assign all values to the appropriate treatment
#As in pathway plots for main text, we convert the log2 fold change to absolute and normalise those that are a fraction to be negative
abun, P, PhAc, labels = [], [], [], []
for a in range(len(rows)):
    if a > 0:
        for b in range(len(rows[a])):
            if b > 0:
                rows[a][b] = float(rows[a][b])
                if b > 5:
                    rows[a][b] = math.pow(2, rows[a][b])
                    if rows[a][b] < 1:
                        rows[a][b] = -(1/rows[a][b])
        labels.append(rows[a][0])
        abun.append(rows[a][1:6])
        P.append(rows[a][6:10])
        PhAc.append(rows[a][10:])

#Get the color maps for up and down fold change   
cmap_up = 'seismic'
norm_up = mpl.colors.Normalize(vmin=-8, vmax=10)
colormap_up = mpl.cm.get_cmap(cmap_up, 256)
m_up = mpl.cm.ScalarMappable(norm=norm_up, cmap=colormap_up)
cmap_down = 'seismic'
norm_down = mpl.colors.Normalize(vmin=-10, vmax=8)
colormap_down = mpl.cm.get_cmap(cmap_down, 256)
m_down = mpl.cm.ScalarMappable(norm=norm_down, cmap=colormap_down)

#As in the pathway plots for the main text, remove the frames that we don't want and the ticks
def remove(xy, ax):
    if xy == 'x':
        ax.tick_params(axis='x',which='both',top='off', bottom='off')
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax, xticks=[], xticklabels=[])
    elif xy == 'y':
        ax.tick_params(axis='y',which='both',left='off', right='on')
    return

for a in range(len(abun)):
    fig = plt.figure(figsize=(5,4))
    #We are looking at the fold changes with the positive control (P above, and not those with phthalic acid, PhAc above)
    PhAc, DBP, DEHP, ATBC = P[a][0], P[a][1], P[a][2], P[a][3]
    #Getting the values for abundance, too
    PhAc_a, DBP_a, DEHP_a, ATBC_a = abun[a][1], abun[a][2], abun[a][3], abun[a][4]
    ax = plt.subplot(121)
    fs=40
    #Plot the fold change colors for each of the treatments, changing text color to white if need be
    #Then add the text showing the value of this fold change
    if ATBC > 0:
        ax.bar([1], [1], color=[m_up.to_rgba(ATBC)], width=1)
        if ATBC > (7.5):tx = 'w'
        else:tx = 'k'
    else:
        if ATBC < (-4):tx = 'w'
        else:tx = 'k'
        ax.bar([1], [1], color=[m_down.to_rgba(ATBC)], width=1)
    ax.text(1, 0.5, str(round(ATBC,1)), color=tx, fontsize=fs, ha='center', va='center')
    if DEHP > 0:
        ax.bar([1], [1], color=[m_up.to_rgba(DEHP)], bottom=[1], width=1)
        if DEHP > (7.5):tx = 'w'
        else:tx = 'k'
    else:
        if DEHP < (-4):tx = 'w'
        else:tx = 'k'
        ax.bar([1], [1, 1], color=[m_down.to_rgba(DEHP)], bottom=[1], width=1)
    ax.text(1, 1.5, str(round(DEHP,1)), color=tx, fontsize=fs, ha='center', va='center')
    if DBP > 0:
        ax.bar([1], [1], color=[m_up.to_rgba(DBP)], bottom=[2], width=1)
        if DBP > (7.5):tx = 'w'
        else:tx = 'k'
    else:
        if DBP < (-4):tx = 'w'
        else:tx = 'k'
        ax.bar([1], [1], color=[m_down.to_rgba(DBP)], bottom=[2], width=1)
    ax.text(1, 2.5, str(round(DBP,1)), color=tx, fontsize=fs, ha='center', va='center')
    if PhAc > 0:
        ax.bar([1], [1], color=[m_up.to_rgba(PhAc)], bottom=[3], width=1)
        if PhAc > (7.5):tx = 'w'
        else:tx = 'k'
    else:
        if PhAc < (-4):tx = 'w'
        else:tx = 'k'
        ax.bar([1], [1], color=[m_down.to_rgba(PhAc)], bottom=[3], width=1)
    ax.text(1, 3.5, str(round(PhAc,1)), color=tx, fontsize=fs, ha='center', va='center')
    #Now add the y labels showing the treatment and relative abundance within that treatment, and add horizontal lines to separate each treatment
    y_lab = ['ATBC ('+str(round(ATBC_a,2))+'%)', 'DEHP ('+str(round(DEHP_a,2))+'%)', 'DBP ('+str(round(DBP_a,2))+'%)', 'PhAc ('+str(round(PhAc_a,2))+'%)']
    remove('x', ax), remove('y', ax)
    ax.plot([0.5,2.5], [1,1], 'k-')
    ax.plot([0.5,2.5], [2,2], 'k-')
    ax.plot([0.5,2.5], [3,3], 'k-')
    ax.yaxis.tick_right()
    plt.yticks([0.5, 1.5, 2.5, 3.5], y_lab, fontsize=fs)
    ax.set_ylim([0,4])
    ax.set_xlim([0.5,1.5])
    title = title1
    adding = False
    count = 0
    #Add line breaks where necessary in enzyme names
    for b in range(len(labels[a])):
        if labels[a][b] == '_':
            adding = True
        if labels[a][b] == ' ':
            count += 1
            if count == 2:
                title += '\n'
            #elif count == 3:
            #    title += '\n'
            #elif count == 5:
            #    title += '\n'
        if adding:
            title += labels[a][b]
    #Add the title and save the plot
    ax.text(2.2, 4.3, title[2:], fontsize=fs, ha='center', va='bottom', color=fc)
    for b in range(len(labels[a])):
        if labels[a][b] == '/':
            labels[a] = labels[a][:b]+'_'+labels[a][b+1:]
    fig.set_facecolor('#FFC000')
    fig.savefig(labels[a]+'.png', bbox_inches='tight', facecolor='#FFC000')
    plt.close()


#Make a colorbar
ax1 = plt.subplot2grid((6,1), (0,0), colspan=1, frameon=False)
norm = mpl.colors.Normalize(vmin=0, vmax=1)
cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=plt.cm.seismic, norm=norm, orientation='horizontal')
ax1.text(0.5,1, 'Fold change', ha='center', va='bottom', fontsize=fs)
cb1.set_ticks([0, 1])
cb1.set_ticklabels(['<-10', '>10'])
cb1.ax.tick_params(labelsize=fs-10)
plt.savefig('Colorbar.png', bbox_inches='tight', dpi=600)
plt.close()