import csv
import numpy
from scipy import stats
import math


#The input file name can be either: Hcamp_cellular_from_Perseus.csv, Hcamp_exo_from_Perseus.csv, Mhous_cellular_from_Perseus.csv, Mhous_exo_from_Perseus.csv
fn = 'Hcamp_cellular_from_Perseus.csv'
beg = 'HC'

#File name to save this as - currently just a modification of the original file name
new_fn = fn[:-4]+'_fc.csv'

with open(fn, 'rU') as f:
    rows = []
    for row in csv.reader(f):
        rows.append(row)

#Column headers
means, sd, fc, t_test, t_test_sig, t_test_PhAc, t_test_PhAc_sig, rel_abun, fc_PhAc = [['P_mean', 'PhAc_mean', 'DBP_mean', 'DEHP_mean', 'ATBC_mean']], [['P_sd', 'PhAc_sd', 'DBP_sd', 'DEHP_sd', 'ATBC_sd']], [['P_PhAc_fc', 'P_DBP_fc', 'P_DEHP_fc', 'P_ATBC_fc']], [['P_PhAc_ttest', 'P_DBP_ttest', 'P_DEHP_ttest', 'P_ATBC_ttest']], [['P_PhAc_ttest_sig', 'P_DBP_ttest_sig', 'P_DEHP_ttest_sig', 'P_ATBC_ttest_sig']], [['PhAc_DBP_ttest', 'PhAc_DEHP_ttest', 'PhAc_ATBC_ttest']], [['PhAc_DBP_ttest_sig', 'PhAc_DEHP_ttest_sig', 'PhAc_ATBC_ttest_sig']], [['P_relabun', 'PhAc_relabun', 'DBP_relabun', 'DEHP_relabun', 'ATBC_relabun']], [['PhAc_DBP_fc', 'PhAc_DEHP_fc', 'PhAc_ATBC_fc']], 

#Turn the numbers from the csv file into float type
for a in range(len(rows)):
    for b in range(len(rows[a])):
        if a > 0 and b > 0:
            rows[a][b] = float(rows[a][b])
   
#For each of the proteins in the original file     
for a in range(len(rows)):
    if a > 0:
        #Define which of the columns belongs to which treatment and calculate mean and standard deviation of each of these
        P, PhAc, DBP, DEHP, ATBC = [rows[a][1], rows[a][2], rows[a][3]], [rows[a][4], rows[a][5], rows[a][6]], [rows[a][7], rows[a][8], rows[a][9]], [rows[a][10], rows[a][11], rows[a][12]], [rows[a][13], rows[a][14], rows[a][15]]
        P_mean, PhAc_mean, DBP_mean, DEHP_mean, ATBC_mean = numpy.mean(P), numpy.mean(PhAc), numpy.mean(DBP), numpy.mean(DEHP), numpy.mean(ATBC)
        this_means = [P_mean, PhAc_mean, DBP_mean, DEHP_mean, ATBC_mean]
        this_sd = [numpy.std(P),
                      numpy.std(PhAc),
                      numpy.std(DBP),
                      numpy.std(DEHP),
                      numpy.std(ATBC)]
        means.append(this_means)
        sd.append(this_sd)
        this_fc, this_fc_PhAc = [], []
        #Calculate fold changes for each of these with the positive control
        this_fc.append((PhAc_mean-P_mean)), this_fc.append((DBP_mean-P_mean)), this_fc.append((DEHP_mean-P_mean)), this_fc.append((ATBC_mean-P_mean))
        fc.append(this_fc)
        #Now calculate fold changes for each of the plasticizers with phthalic acid
        this_fc_PhAc.append((DBP_mean-PhAc_mean)), this_fc_PhAc.append((DEHP_mean-PhAc_mean)), this_fc_PhAc.append((ATBC_mean-PhAc_mean))
        fc_PhAc.append(this_fc_PhAc)
        #Carry out T-tests for significance and save only the P value of each of these
        this_ttest = [stats.ttest_ind(P,PhAc)[1], stats.ttest_ind(P,DBP)[1], stats.ttest_ind(P,DEHP)[1], stats.ttest_ind(P,ATBC)[1]]
        t_test.append(this_ttest)
        this_ttest_PhAc = [stats.ttest_ind(PhAc,DBP)[1], stats.ttest_ind(PhAc,DEHP)[1], stats.ttest_ind(PhAc,ATBC)[1]]
        t_test_PhAc.append(this_ttest_PhAc)
        this_ttest_sig, this_ttest_PhAc_sig = [], []
        #Now add '+' symbols to a column of the file if the T-test was significant (p<0.05)
        for b in range(len(this_ttest)):
            if this_ttest[b] <= 0.05:
                this_ttest_sig.append('+')
            else:
                this_ttest_sig.append('')
        for c in range(len(this_ttest_PhAc)):
            if this_ttest_PhAc[c] <= 0.05:
                this_ttest_PhAc_sig.append('+')
            else:
                this_ttest_PhAc_sig.append('')
        t_test_sig.append(this_ttest_sig)
        t_test_PhAc_sig.append(this_ttest_PhAc_sig)
                
#Now calculate the sum of each of the columns
sums = []
for a in range(len(means[0])):
    count = 0
    for b in range(len(means)):
        if b > 0:
             count += math.pow(2, means[b][a])
    sums.append(count)

#And add a column to each protein that shows relative abundance of that protein within the proteome of each treatment
for a in range(len(means)):
    if a > 0:
        this_rel_abun = []
        for b in range(len(means[a])):
            this_rel_abun.append((math.pow(2, means[a][b])/sums[b])*100)
        rel_abun.append(this_rel_abun)
    
#And save all of this to a .csv file, with a name as set at the beginning of the file
with open(new_fn, 'w') as f:
    writer = csv.writer(f)
    for a in range(len(rows)):
        writer.writerow(rows[a]+rel_abun[a]+means[a]+sd[a]+fc[a]+fc_PhAc[a]+t_test[a]+t_test_sig[a]+t_test_PhAc[a]+t_test_PhAc_sig[a])
