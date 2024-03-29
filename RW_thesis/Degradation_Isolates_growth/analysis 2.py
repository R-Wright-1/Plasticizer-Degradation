#isolate growth
import matplotlib.pyplot as plt
import numpy
import csv
from colorsys import hls_to_rgb
import random

f = 'Isolates growth different substrates2.csv'

with open(f, 'rU') as f:
    rows = []
    for row in csv.reader(f):
        rows.append(row)
control, b1, b2, b3, times, time = [], [], [], [], [], 0
del rows[0:28]

for a in range(len(rows[0])):
    if a > 2:
        this_rep = []
        for b in range(134):
            if a == 5:
                times.append(time)
                time += 0.5
            this_rep.append(float(rows[b][a]))
        if 14 < a < 45:
            b1.append(this_rep)
        elif 50 < a < 81:
            b2.append(this_rep)

            
    
def get_distinct_colors(n):
    colors = []
    for i in numpy.arange(0., 360., 360. / n):
        h = i / 360.
        l = (50 + numpy.random.rand() * 10) / 100.
        s = (90 + numpy.random.rand() * 10) / 100.
        colors.append(hls_to_rgb(h, l, s))
    random.shuffle(colors)
    return colors

def sep_plots(bac, name, colors, title):
    names = ['No carbon', 'Glucose', 'Succinate', 'Pyruvate', 'Glycerol', 'GlcNAc', 'BHET', 'Fructose', 'Phthalic acid', 'Marine broth']
    if bac == b1:
        ax1 = plt.subplot(221)
        ax2 = plt.subplot(222, sharey=ax1)
    elif bac == b2:
        ax1 = plt.subplot(223)
        ax2 = plt.subplot(224, sharey=ax1)
    ax = [ax1, ax2]
    xlabels = [0, 24, 48, 72]
    count = 0
    for a in range(len(bac)):
        n = a % 3
        if bac == b1:
            if n == 1:
                ax[n].plot(times, bac[a], color=colors[count], label=names[count])
                count += 1
                ax[n].set_xticks(xlabels)
            elif n == 0:
                ax[n].plot(times, bac[a], color=colors[count])
                ax[n].set_xticks(xlabels)
        elif bac == b2:
            if n == 2:
                n = 1
                ax[n].plot(times, bac[a], color=colors[count], label=names[count])
                count += 1
                ax[n].set_xticks(xlabels)
            elif n == 1:
                n = 0
                ax[n].plot(times, bac[a], color=colors[count])
                ax[n].set_xticks(xlabels)
    if bac == b1:
        ax[1].legend(bbox_to_anchor=(1, 1.05))
    ax1.set_title('1', loc='left')
    ax2.set_title('2', loc='left')
    label = title+'\n Absorbance (600 nm)'
    ax1.set_ylabel(label)  
    if bac == b2:
        ax1.set_xlabel('Hours')
        ax2.set_xlabel('Hours')
    plt.setp(ax2.get_yticklabels(), visible=False)
    return

fig = plt.figure(figsize=(10,7.5))
colors = ['k']+get_distinct_colors(10)
sep_plots(b1, 'Bac 1 oct', colors, r'$Halomonas$'+' sp. ATBC28')
sep_plots(b2, 'Bac 2 oct', colors, r'$Mycobacterium$'+' sp. DBP42')
plt.tight_layout()
plt.savefig('Both bacteria.png', bbox_inches='tight', dpi=600)
plt.close()