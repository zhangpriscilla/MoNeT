"""
Graph difference between noaggregation and some level of aggregation CSV result files . 
Plot the error (delta/noagg) of the homing H allele over time, treating no aggregation as truth.
"""

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from visualizeMultiple import alleleCounts
from pathlib import Path
from sklearn.metrics import mean_squared_error
from math import sqrt


def rmse(predictions, targets):
	diff = predictions - targets
	diff = diff ** 2
	diff = diff.mean()
	diff = np.sqrt(diff)
	diff = diff / predictions.mean()
	return diff


counts1 = 0
counts2 = 0
counts3 = 0
def plotHAllele(pathlist, counts, name):
	count = 0
	total = set()
	for path in pathlist:
		path_in_str = str(path)
		total.add(path_in_str)
		if count == 0:
			count = 1
			counts = alleleCounts(path_in_str, ['H', 'W', 'B', 'R'])[0]
		else:
			h_allele = alleleCounts(path_in_str, ['H', 'W', 'B', 'R'])[0]
			counts = np.add(counts, h_allele)
	plt.plot(counts, label=name)
	return counts


pathlist = Path("/Users/gillianchu/Desktop/MGDrive-Experiments/Experiments/Oct25/noagg/2018_10_15_ANALYZED/E_080_000_000_000/").glob('**/*.csv')
counts1 = plotHAllele(pathlist, counts1, "No Aggregation")

pathlist = Path("/Users/gillianchu/Desktop/MGDrive-Experiments/Experiments/Oct25/fullagg/2018_10_15_ANALYZED/E_080_000_000_000/").glob('**/*.csv')
counts2 = plotHAllele(pathlist, counts2, "Full Aggregation")

pathlist = Path("/Users/gillianchu/Desktop/MGDrive-Experiments/Experiments/Oct25/halfagg/2018_10_15_ANALYZED/E_080_000_000_000/").glob('**/*.csv')
counts3 = plotHAllele(pathlist, counts3, "Half Aggregation")

# rms0 = rmse(np.array(counts1), np.array(counts1))
# print('RMSE of No Aggregation against No Aggregation: ', rms0)

# rmse_full = rmse(np.array(counts2), np.array(counts1))
# print('RMSE of No Aggregation against Full Aggregation: ', rmse_full)

# rmse_half = rmse(np.array(counts3), np.array(counts1))
# print('RMSE of No Aggregation against Half Aggregation: ', rmse_half)

# plt.legend()
# plt.show()

def entropy(predictions, targets):
	"""
		Y = fx(X1, X2, X3, X4 ...)
		I(X ; Y) = H(X) - H(Y|X)
		vs. 
		I(X1, X2, X3, X4, ... ; Y) = H(X1, X2, X3, X4, ... ; Y))
	"""

	return
