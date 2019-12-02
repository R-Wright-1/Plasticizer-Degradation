import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

#Colors for text for 'Halo' and 'Myco' labels
Hcol, Mcol = '#F4B183', '#9DC3E6'

#Each box of the pathway is basically a stacked bar plot, plotted on a figure/axis
#Function to remove the normal frame and tick lines etc. Also adds the Halo/Myco labels and the genome position of that protein
def remove(ax, fs, myco, halo):
    ax.tick_params(axis='x',which='both',top='on', bottom='off')
    ax.xaxis.tick_top()
    plt.xticks([])
    ax.text(0, 3.1, 'Myco\n', fontsize=fs, color=Mcol, va='bottom', ha='center')
    ax.text(0, 3.1, myco, fontsize=fs-5, color='k', va='bottom', ha='center')
    ax.text(1.5, 3.1, 'Halo\n', fontsize=fs, color=Hcol, va='bottom', ha='center')
    ax.text(1.5, 3.1, halo, fontsize=fs-5, color='k', va='bottom', ha='center')
    plt.yticks([])
    ax.tick_params(axis='y',which='both',left='off', right='off')
    ax.yaxis.tick_right()
    return

#Add fold change plots to axis
def get_plot(n1, n2, name, fs, halo, myco, enzyme):
    #Reverse fold change values because we plot from the bottom
    n1.reverse()
    n2.reverse()
    #Color maps are arranged to make sure there is not too much white around 0
    cmap_up = 'seismic'
    norm_up = mpl.colors.Normalize(vmin=-8, vmax=10)
    colormap_up = mpl.cm.get_cmap(cmap_up, 256)
    m_up = mpl.cm.ScalarMappable(norm=norm_up, cmap=colormap_up)
    cmap_down = 'seismic'
    norm_down = mpl.colors.Normalize(vmin=-10, vmax=8)
    colormap_down = mpl.cm.get_cmap(cmap_down, 256)
    m_down = mpl.cm.ScalarMappable(norm=norm_down, cmap=colormap_down)
    #Get figure and subplot
    plt.figure(figsize=(6,4))
    ax1 = plt.subplot(111, frameon=False)
    txt = ['ATBC\n', 'DEHP\n', 'DBP\n']
    #For each fold change value, get the corresponding color from the colormap and change the text color to white/black depending
    #on how dark the color is and which will be most easily visible
    for a in range(len(n1)):
        tx1, tx2 = 'k', 'k'
        edge1, edge2 = 'k', 'k'
        if n1[a] == 'ND':
            color1, edge1 = 'w', 'w'
        elif n1[a] > 0:
            color1 = m_up.to_rgba(n1[a])
            if n1[a] > 7.5: tx1 = 'w'
        else:
            color1 = m_down.to_rgba(n1[a])
        if n2[a] == 'ND':
            color2, edge2 = 'w', 'w'
        elif n2[a] > 0:
            color2 = m_up.to_rgba(n2[a])
            if n2[a] > 7.5: tx2 = 'w'
        else: 
            color2 = m_down.to_rgba(n2[a])
        #Plot these bars, leaving a gap in between them where the arrow will go in the figure
        if a > 0:
            ax1.bar([0,1.5], [1,1], bottom=[a, a], color=[color1, color2], width=[0.99,0.99], edgecolor=[edge1, edge2])
        else:
            ax1.bar([0,1.5], [1,1], width=[0.99,0.99], edgecolor=[edge1, edge2], color=[color1, color2])
        #If the protein was detected, add text showing the fold change (to 1 decimal place)
        if n1[a] != 'ND':
            ax1.text(0, a+0.5, txt[a]+str(round(n1[a], 1)), color=tx1, fontsize=fs-12, ha='center', va='center')
        if n2[a] != 'ND':
            ax1.text(1.5, a+0.5, txt[a]+str(round(n2[a], 1)), color=tx2, fontsize=fs-12, ha='center', va='center')
    #Change x and y limits, add the text on the side showing the name of this enzyme and call the above function to remove axis frame
    #and add text labels etc.
    ax1.set_xlim([-0.5, 2])
    ax1.set_ylim([0, 3])
    ax1.text(2.4, 1.5, enzyme, fontsize=fs-15, color='k', ha='center', va='center', rotation=90)
    remove(ax1, fs, myco, halo)
    plt.savefig(name+'.png', bbox_inches='tight', dpi=300)
    plt.close()
    return

fs = 44

#Function to check whether we have a number or not
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Get information from csv file
with open('Pathways_confirmed.csv', 'rU') as f:
    rows = []
    for row in csv.reader(f):
        rows.append(row)

#Go through each line of this csv file and get the info for each bacterium, including position of this protein in the genome,
#whether we are plotting a pathway or individual protein and fold change (or not if it wasn't detected)
for a in range(1, len(rows)):
    nums = rows[a][4:-1] #fold change values
    name = rows[a][0] #name to save this figure with/which part of the pathway this describes
    halo, myco = rows[a][2], rows[a][1] #genome positions in halo and myco
    enzyme = rows[a][-1] #name of the enzyme e.g. Phthalate 3,4-dioxygenase
    #If the genome positions are longer than 5 characters, then they are for multiple enzymes and we should write 'multiple'
    #instead of the genome position
    if len(halo) > 5:
        halo = 'Multiple'
    elif halo != '' and halo != 'ND':
        halo = str(int(halo)).zfill(4)
    if len(myco) > 5:
        myco = 'Multiple'
    elif myco != '' and myco != 'ND':
        myco = str(int(myco)).zfill(4)
    new_enzyme = ''
    #Get the enzyme name in an easily readable format
    #If we have underscores in the name, add line breaks so that the name fits nicely on the side
    for a in range(len(enzyme)):
        if enzyme[a] == '_':
            new_enzyme += '\n'
        else:
            new_enzyme += enzyme[a]
    #If we have values for the numbers and if they are numbers (checked by above function) and they are not equal to 'ND'
    if nums != ['', '', '', '', '', '']:
        for b in range(len(nums)):
            if is_number(nums[b]) and nums[b] != 'ND':
                nums[b] = float(nums[b]) #Turn them into a float (rather than string)
                nums[b] = math.pow(2, nums[b]) #Convert them to an absolute fold change, rather than the current log2 fold change
                if nums[b] < 1: #If they are below 1, then convert this to be a negative fold change rather than a fraction
                    nums[b] = -(1/nums[b])
        #And then get the plot
        get_plot(nums[:3], nums[3:], name, fs, halo, myco, new_enzyme)
