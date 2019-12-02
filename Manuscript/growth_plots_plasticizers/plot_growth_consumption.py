import csv
import numpy
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

#Colors to use for plots and x values for growth (days) and bar plot (arbitrary)
Hcol, Mcol = '#F4B183', '#9DC3E6'
x = [0, 1, 2, 4, 7]
xbar = [1, 2.5, 3.5, 5, 6]
colorbar = ['k', Mcol, '#ebf3fa', Hcol, '#fceadd']

#Values calculated by previous "plot_growth.py" script - growth measured as absorbance at 600 nm
labile_halo, labile_halo_error = [0.04, 0.09966666666666667, 0.1406666666666667, 0.145, 0.13933333333333334], [0, 0.004642796092394704, 0.004642796092394698, 0.004966554808583784, 0.010530379332620873]
labile_myco, labile_myco_error = [0.04, 0.04, 0.043000000000000003, 0.048999999999999995, 0.12233333333333334], [0, 0.0008164965809277268, 0.004242640687119286, 0.003559026084010437, 0.05060522590492891]

pa_halo, pa_halo_error = [0.04, 0.04633333333333334, 0.046000000000000006, 0.04900000000000001, 0.04733333333333334], [0, 0.0020548046676563273, 0.0021602468994692888, 0.002943920288775949, 0.0012472191289246482]
pa_myco, pa_myco_error = [0.04, 0.04066666666666666, 0.043666666666666666, 0.044333333333333336, 0.04800000000000001], [0, 0.00047140452079103207, 0.002867441755680875, 0.0016996731711975933, 0.0037416573867739417]

dbp_halo, dbp_halo_error = [0.04, 0.067, 0.08, 0.09233333333333334, 0.07633333333333332], [0, 0.0053541261347363365, 0.009092121131323901, 0.012472191289246471, 0.003299831645537225]
dbp_myco, dbp_myco_error = [0.04, 0.05566666666666667, 0.07766666666666668, 0.08633333333333333, 0.12], [0, 0.00047140452079103207, 0.00903081145609604, 0.006649979114420001, 0.010708252269472677]

dehp_halo, dehp_halo_error = [0.04, 0.05633333333333334, 0.05833333333333333, 0.066, 0.13999999999999999], [0, 0.0012472191289246482, 0.0016996731711975933, 0.0014142135623730965, 0.06125357132445421]
dehp_myco, dehp_myco_error = [0.04, 0.05000000000000001, 0.06266666666666666, 0.07533333333333335, 0.12333333333333334], [0, 0.005715476066494083, 0.006599663291074447, 0.008055363982396382, 0.014055445761538669]

atbc_halo, atbc_halo_error = [0.04, 0.069, 0.08733333333333333, 0.08800000000000001, 0.10200000000000002], [0, 0.004898979485566355, 0.008956685895029603, 0.0014142135623730961, 0.010801234497346436]
atbc_myco, atbc_myco_error = [0.04, 0.05333333333333334, 0.06, 0.06266666666666666, 0.06933333333333334], [0, 0.0009428090415820641, 0.009201449161228172, 0.005906681715556447, 0.009030811456096046]

#Values taken directly from excel Table S7C - peak area as measured by metabolomics
pa, pa_sd = [9.25E+07, 2.64E+08, 0, 2.93E+08, 0], [9.90E+04, 2.40E+06, 0, 5.52E+06, 0]
dbp, dbp_sd = [8.04E+06, 0, 0, 0, 0], [2.83E+03, 0, 0, 0, 0]
dehp, dehp_sd = [4.50E+08, 6.27E+06, 6.58E+06, 6.97E+06, 6.40E+06], [1.85E+07, 8.70E+04, 8.16E+05, 7.07E+04, 7.62E+05]
atbc, atbc_sd = [7.11E+07, 1.80E+07, 1.93E+07, 1.88E+07, 1.90E+07], [2.11E+06, 1.84E+05, 4.03E+05, 8.49E+05, 2.07E+06]

#Set up figure and axis
plt.figure(figsize=(10, 6))

ax1, ax2, ax3, ax4, ax5 = plt.subplot2grid((2, 11), (0, 1), colspan=2), plt.subplot2grid((2, 11), (0, 3), colspan=2), plt.subplot2grid((2, 11), (0, 5), colspan=2), plt.subplot2grid((2, 11), (0, 7), colspan=2), plt.subplot2grid((2, 11), (0, 9), colspan=2)
ax6, ax7, ax8, ax9 = plt.subplot2grid((2, 44), (1, 13), colspan=6), plt.subplot2grid((2, 44), (1, 21), colspan=6), plt.subplot2grid((2, 44), (1, 29), colspan=6), plt.subplot2grid((2, 44), (1, 37), colspan=6)
ax1.set_title('Labile substrate'), ax2.set_title('Phthalic acid'), ax3.set_title('DBP'), ax4.set_title('DEHP'), ax5.set_title('ATBC')
ax1.set_ylabel('Growth\nAbsorbance (600 nm)')
ax6.set_ylabel('Substrate consumption\nPeak area')

#Plot growth with means and standard deviations
ax1.errorbar(x, labile_myco, yerr=labile_myco_error, color=Mcol, marker='^', linestyle='-', capsize=3, markeredgecolor='k'), ax1.errorbar(x, labile_halo, yerr=labile_halo_error, color=Hcol, marker='o', linestyle='--', capsize=3, markeredgecolor='k')
ax2.errorbar(x, pa_myco, yerr=pa_myco_error, color=Mcol, marker='^', linestyle='-', capsize=3, markeredgecolor='k'), ax2.errorbar(x, pa_halo, yerr=pa_halo_error, color=Hcol, marker='o', linestyle='--', capsize=3, markeredgecolor='k')
ax3.errorbar(x, dbp_myco, yerr=dbp_myco_error, color=Mcol, marker='^', linestyle='-', capsize=3, markeredgecolor='k'), ax3.errorbar(x, dbp_halo, yerr=dbp_halo_error, color=Hcol, marker='o', linestyle='--', capsize=3, markeredgecolor='k')
ax4.errorbar(x, dehp_myco, yerr=dehp_myco_error, color=Mcol, marker='^', linestyle='-', capsize=3, markeredgecolor='k'), ax4.errorbar(x, dehp_halo, yerr=dehp_halo_error, color=Hcol, marker='o', linestyle='--', capsize=3, markeredgecolor='k')
ax5.errorbar(x, atbc_myco, yerr=atbc_myco_error, color=Mcol, marker='^', linestyle='-', capsize=3, markeredgecolor='k'), ax5.errorbar(x, atbc_halo, yerr=atbc_halo_error, color=Hcol, marker='o', linestyle='--', capsize=3, markeredgecolor='k')

#Plot bars showing substrate consumption/peak area
ax7.bar([1], [pa[0]/9], color='k', alpha=0) #This bar is invisible, and is just to put the axis on the correct scale
paplt, dbpplt, dehpplt, atbcplt = ax6.bar(xbar, pa, yerr=pa_sd, color=colorbar, edgecolor='k', ecolor='k', capsize=3), ax7.bar(xbar, dbp, yerr=dbp_sd, color=colorbar, edgecolor='k', ecolor='k', capsize=3), ax8.bar(xbar, dehp, yerr=dehp_sd, color=colorbar, edgecolor='k', ecolor='k', capsize=3), ax9.bar(xbar, atbc, yerr=atbc_sd, color=colorbar, edgecolor='k', ecolor='k', capsize=3)
paplt[2].set_hatch('//'), paplt[4].set_hatch('//'), dbpplt[2].set_hatch('//'), dbpplt[4].set_hatch('//'), dehpplt[2].set_hatch('//'), dehpplt[4].set_hatch('//'), atbcplt[2].set_hatch('//'), atbcplt[4].set_hatch('//')

#Set higher y limits for the axis, to allow for labels
ax1.set_ylim([0.025, 0.178]), ax2.set_ylim([0.025, 0.178]), ax3.set_ylim([0.025, 0.178]), ax4.set_ylim([0.025, 0.178]), ax5.set_ylim([0.025, 0.178])

#Add labels to the bars and format x ticks etc
xbar = [1, 2.5, 3.5, 5, 6]#
ax6.plot([0.6, 1.4], [3.25E+08, 3.25E+08], 'k-'), ax6.plot([2.1, 3.9], [3.25E+08, 3.25E+08], 'k-'), ax6.plot([4.6, 6.4], [3.25E+08, 3.25E+08], 'k-')
ax7.plot([0.6, 1.4], [0.975E+07, 0.975E+07], 'k-'), ax7.plot([2.1, 3.9], [0.975E+07, 0.975E+07], 'k-'), ax7.plot([4.6, 6.4], [0.975E+07, 0.975E+07], 'k-')
ax8.plot([0.6, 1.4], [4.875E+08, 4.875E+08], 'k-'), ax8.plot([2.1, 3.9], [4.875E+08, 4.875E+08], 'k-'), ax8.plot([4.6, 6.4], [4.875E+08, 4.875E+08], 'k-')
ax9.plot([0.6, 1.4], [7.7E+07, 7.7E+07], 'k-'), ax9.plot([2.1, 3.9], [7.7E+07, 7.7E+07], 'k-'), ax9.plot([4.6, 6.4], [7.7E+07, 7.7E+07], 'k-')
plt.setp(ax6, yticks=[0E+08, 1E+08, 2E+08, 3E+08], yticklabels=['0', '1', '2', '3'])
plt.setp(ax7, yticks=[0E+07, 0.2E+07, 0.4E+07, 0.6E+07, 0.8E+07, 1.0E+07], yticklabels=['0', '0.2', '0.4', '0.6', '0.8', '1.0'])
plt.setp(ax8, yticks=[0E+08, 1E+08, 2E+08, 3E+08, 4E+08, 5E+08], yticklabels=['0', '1', '2', '3', '4', '5'])
plt.setp(ax9, yticks=[0E+07, 2E+07, 4E+07, 6E+07, 8E+07], yticklabels=['0', '2', '4', '6', '8'])
ax6.text(-1.5, 4E+08, '1e8')
ax7.text(-1.5, 1.2E+07, '1e7')
ax8.text(-1.5, 6E+08, '1e8')
ax9.text(-1.5, 9.5E+07, '1e7')
ax6.text(1, 3.3E+08, 'No\ninoc', ha='center', va='bottom', fontsize=7), ax6.text(3, 3.3E+08, 'Myco', ha='center', va='bottom', fontsize=7), ax6.text(5.5, 3.3E+08, 'Halo', ha='center', va='bottom', fontsize=7)
ax7.text(1, 0.99E+07, 'No\ninoc', ha='center', va='bottom', fontsize=7), ax7.text(3, 0.99E+07, 'Myco', ha='center', va='bottom', fontsize=7), ax7.text(5.5, 0.99E+07, 'Halo', ha='center', va='bottom', fontsize=7)
ax8.text(1, 4.95E+08, 'No\ninoc', ha='center', va='bottom', fontsize=7), ax8.text(3, 4.95E+08, 'Myco', ha='center', va='bottom', fontsize=7), ax8.text(5.5, 4.95E+08, 'Halo', ha='center', va='bottom', fontsize=7)
ax9.text(1, 7.818E+07, 'No\ninoc', ha='center', va='bottom', fontsize=7), ax9.text(3, 7.818E+07, 'Myco', ha='center', va='bottom', fontsize=7), ax9.text(5.5, 7.818E+07, 'Halo', ha='center', va='bottom', fontsize=7)
ax6.set_ylim([0E+08, 4E+08]), ax7.set_ylim([0E+07, 1.2E+07]), ax8.set_ylim([0E+08, 6E+08]), ax9.set_ylim([0E+07, 9.5E+07])
ax2.set_yticks([]), ax3.set_yticks([]), ax4.set_yticks([]), ax5.set_yticks([])#, ax7.set_yticks([]), ax8.set_yticks([]), ax9.set_yticks([])
ax1.set_xticks(x), ax2.set_xticks(x), ax3.set_xticks(x), ax4.set_xticks(x), ax5.set_xticks(x)
xbplt = [1, 2.5, 3.5, 5, 6]
xblab = ['+', '+', '-', '+', '-']
plt.setp(ax6, xticks=xbplt, xticklabels=xblab)
plt.setp(ax7, xticks=xbplt, xticklabels=xblab)
plt.setp(ax8, xticks=xbplt, xticklabels=xblab)
plt.setp(ax9, xticks=xbplt, xticklabels=xblab)
ax6.set_xlabel('Phthalic acid'), ax7.set_xlabel('DBP'), ax8.set_xlabel('DEHP'), ax9.set_xlabel('ATBC')
ax3.set_xlabel('Days')
ax6.text(xbar[2], 0.1E+08, 'ND', color='gray', fontsize=8, rotation=90, va='bottom', ha='center')
ax6.text(xbar[4], 0.1E+08, 'ND', color='gray', fontsize=8, rotation=90, va='bottom', ha='center')
ax7.text(xbar[1], 0.03E+07, 'ND', color='gray', fontsize=8, rotation=90, va='bottom', ha='center')
ax7.text(xbar[2], 0.03E+07, 'ND', color='gray', fontsize=8, rotation=90, va='bottom', ha='center')
ax7.text(xbar[3], 0.03E+07, 'ND', color='gray', fontsize=8, rotation=90, va='bottom', ha='center')
ax7.text(xbar[4], 0.03E+07, 'ND', color='gray', fontsize=8, rotation=90, va='bottom', ha='center')

#Add a separate axis for the legend (manually added)
axleg = plt.subplot2grid((2, 22), (1, 0), colspan=2, frameon=False)
axleg.scatter(1.5, 4.5, marker='^', color=Mcol, s=50, edgecolor='k')
axleg.barh([4], [1.3], left=[0.8], color=Mcol, height=0.3, edgecolor='k')
axleg.scatter(1.5, 3.25, marker='o', color=Hcol, s=50, edgecolor='k')
axleg.barh([2.75], [1.3], left=[0.8], color=Hcol, height=0.3, edgecolor='k')
axleg.barh([1.75], [1.3], left=[0.8], color='k', height=0.3, edgecolor='k')
axleg.barh([1.25], [1.3], left=[0.8], color='w', height=0.3, edgecolor='k', hatch='//')
axleg.text(3, 4.25, '$Mycobacterium$ \nsp. DBP42 (Myco)', ha='left', va='center', fontsize=8)
axleg.text(3, 3, '$Halomonas$ \nsp. ATBC28 (Halo)', ha='left', va='center', fontsize=8)
axleg.text(3, 1.75, 'No inoculum', ha='left', va='center', fontsize=8)
axleg.text(3, 1.25, 'No plasticizer', ha='left', va='center', fontsize=8)
axleg.set_xticks([]), axleg.set_yticks([]), axleg.set_ylim([0,5]), axleg.set_xlim([0,5])

#Save the figure
plt.subplots_adjust(hspace=0.5)
plt.savefig('New plot growth consumption.png', dpi=600, bbox_inches='tight')