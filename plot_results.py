import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def pred_by_distance(basename1, basename2):
    legend1 = '1984 (Entire Year)'
    legend2 = '2014-2015 (October-->October)'
    d1 = np.load("results_" + basename1 + ".npz")
    d2 = np.load("results_" + basename2 + ".npz")
    distances1 = (np.load(basename1 + "_distance_matrix.npy")).flatten()
    distances2 = (np.load(basename2 + "_distance_matrix.npy")).flatten()
    weights1 = abs(d1["weights"].flatten())
    weights2 = abs(d2["weights"].flatten())
    total_wt1 = sum(weights1)
    max_dist1 = distances1.max()
    numbins = 500
    binlims1 = np.linspace(0.0,max_dist1, numbins+1)
    wt_per_bin1 = np.zeros(numbins)
    for i in range(numbins):
	wt_per_bin1[i] = (sum(weights1[np.logical_and(distances1>binlims1[i], distances1<binlims1[i+1])]))/total_wt1
    total_wt2 = sum(weights2)
    max_dist2 = distances2.max()
    binlims2 = np.linspace(0.0,max_dist2, numbins+1)
    wt_per_bin2 = np.zeros(numbins)
    for i in range(numbins):
	wt_per_bin2[i] = (sum(weights2[np.logical_and(distances2>binlims2[i], distances2<binlims2[i+1])]))/total_wt2
    dist_fig = plt.figure(num="dist", figsize=(9, 7), dpi=100, facecolor='w', edgecolor='k')
    plt.plot(binlims1[0:numbins], np.cumsum(wt_per_bin1), 'b', label=legend1)
    plt.plot(binlims2[0:numbins], np.cumsum(wt_per_bin2), 'g', label=legend2)
    plt.title("Evidence of Globalization", fontsize=24)
    plt.ylabel("Cumulative Fraction of Total Prediction Weight", fontsize=18)
    plt.xlabel("Distance Between Country Pairs (km)", fontsize=18)
    plt.legend(loc='lower right')
    plt.savefig('plot_distance.png', bbox_inches='tight')

def var_explained(basename1, basename2):
    legend1 = '1984 (Entire Year)'
    legend2 = '2014-2015 (October-->October)'
    d1 = np.load("results_" + basename1 + ".npz")
    d2 = np.load("results_" + basename2 + ".npz")    
    var_ratio_1 = d1["var_ratio"]
    var_ratio_2 = d2["var_ratio"]
    var_ratio_1 = var_ratio_1[~np.isnan(var_ratio_1)]
    var_ratio_2 = var_ratio_2[~np.isnan(var_ratio_2)]
    var_ratio_trunc_1 = var_ratio_1.copy()
    var_ratio_trunc_2 = var_ratio_2.copy()
    var_ratio_trunc_1[var_ratio_trunc_1<0.0] = 0.0
    var_ratio_trunc_2[var_ratio_trunc_2<0.0] = 0.0
    perf_fig = plt.figure(num="perf", figsize=(9, 7), dpi=100, facecolor='w', edgecolor='k')
    n, bins, patches = plt.hist(var_ratio_trunc_1, 20, normed=0, alpha = 0.5, label = legend1) #, facecolor='green', alpha=0.5)
    plt.xlabel("Fraction Variance in Score Explained by Predictor", fontsize=18)
    plt.ylabel("Number of Countries", fontsize=18)
    plt.title("Predictive Performance", fontsize=24)
    n, bins, patches = plt.hist(var_ratio_trunc_2, 20, normed=0, alpha = 0.5, label = legend2) #, facecolor='green', alpha=0.5)
    plt.legend(loc='upper right')
    plt.savefig('plot_performance.png', bbox_inches='tight')
    plt.show()