import csv
import matplotlib.pyplot as plt
import numpy

#read data from .csv file
with open('phthalic_toxicity.csv', 'rU') as f:
    rows = []
    for row in csv.reader(f):
        rows.append(row)

#set up plots, colors, etc.
ax1 = plt.subplot(221)
ax2, ax3, ax4 = plt.subplot(222), plt.subplot(223), plt.subplot(224)
axis = [ax1, ax2, ax3, ax4]
r, co = [3, 12, 3, 12], [2, 2, 19, 19] #indices for the rows and columns where the data starts for each treatment
ax1.set_title('$Mycobacterium$ sp. DBP42')
ax2.set_title('$Halomonas$ sp. ATBC28')
ax1.set_ylabel('Marine broth\nAbsorbance (600 nm)')
ax3.set_ylabel('Marine broth + 0.1% DBP\nAbsorbance (600 nm)')
colors = ['k', '#ff7f00', '#4daf4a', '#f781bf', '#377eb8']
x = [0, 1, 2, 3, 4]
markers = ['o', '^', 's', '*', '1']
labels = ['0%', '0.02%', '0.1%', '0.4%', '1.6%']

#Cycle through the data for each plot (treatment)
for a in range(4):
    ax = axis[a]
    row, col = r[a], co[a]
    #Tell it which data belongs to which day of measurements
    days = [rows[row][col:col+15], rows[row+1][col:col+15], rows[row+2][col:col+15], rows[row+3][col:col+15], rows[row+4][col:col+15]]
    growth, sd = [[], [], [], [], []], [[], [], [], [], []]
    #Now for each day, get means and standard deviations for each biological triplicate
    for b in range(len(days)):
        count = 0
        trt = []
        for c in range(len(days[b])):
            days[b][c] = float(days[b][c])
            trt.append(days[b][c])
            if (c+1) % 3 == 0:
                growth[count].append(numpy.mean(trt))
                sd[count].append(numpy.std(trt))
                trt = []
                count += 1
    #Plot them - first as a scatter, for the legend, and then with lines in the plot
    for b in range(len(growth)):
        ax.scatter(x, growth[b], marker=markers[b], color=colors[b], label=labels[b])
        ax.errorbar(x, growth[b], yerr=sd[b], marker=markers[b], color=colors[b], capsize=3)
    #Add a legend
    if a == 1:
        ax.legend(bbox_to_anchor=(1.1, 1.05))
    if a == 1 or a == 3:
        ax.set_ylim([-0.1, 1.75])
    else:
        ax.set_ylim([-0.01, 0.3])
#Remove x or y ticks where they're not needed and save the figure
plt.setp(ax1, xticks=[])
plt.setp(ax2, xticks=[])
ax3.set_xlabel('Days')
ax4.set_xlabel('Days')

ax2.text(5.95, 1.8, 'Phthalic acid\nconcentration', ha='center', va='bottom')

plt.savefig('Phthalic acid toxicity.png', dpi=600, bbox_inches='tight')
