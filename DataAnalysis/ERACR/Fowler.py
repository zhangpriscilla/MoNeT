import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import FowlerAux as aux
import vincenty as vn
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering

##############################################################################
# Parameters Setup
##############################################################################
(seed, clustersNo, CLST_METHOD) = (42, 250, 1)
(lifeStayProb, adultMortality) = (.72, .09)
# PLACE = "BakersfieldRiver"
# PATH = "/Volumes/marshallShare/ERACR/Bakersfield/Riverside/clean/"
# LATLONGS = "full2.csv"
PLACE = "Fowler"
PATH = "/Volumes/marshallShare/ERACR/Fowler/"
LATLONGS = "fowler_centroids_ordered.csv"
# PLACE = "Gordonvale"
# PATH = "/Volumes/marshallShare/MGDrivE_Datasets/ThresholdDependent/GeoLocations/Curated/"
# LATLONGS = "YorkeysKnob_03.csv"
# PLACE = "Fowler"
# PATH = "/Volumes/marshallShare/ERACR/Fowler/"
# LATLONGS = "fowler_centroids.csv"
latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')
##############################################################################
# Clustering Algorithms
##############################################################################
if CLST_METHOD == 1:
    clObj = KMeans(
        n_clusters=clustersNo,
        random_state=seed
    )
elif CLST_METHOD == 2:
    clObj = AgglomerativeClustering(
        n_clusters=clustersNo,
        affinity='euclidean',
        compute_full_tree='auto'
    )
elif CLST_METHOD == 3:
    clObj = SpectralClustering(
        n_clusters=clustersNo,
        random_state=seed
    )
clusters = clObj.fit_predict(latlongs)
##############################################################################
# Clustering the pointset
##############################################################################
cLatlongs = aux.appendClustersToLatlongs(latlongs, clusters)
csvPath = PATH + PLACE + "CLS" + str(CLST_METHOD) + ".csv"
aux.exportListToCSV(csvPath, cLatlongs)
##############################################################################
# Plotting
##############################################################################
plt.figure(figsize=(20, 20))
plt.scatter(
    latlongs[:, 0], latlongs[:, 1], c=clusters,
    alpha=.25, cmap='hsv', s=150, linewidth=4
)
plt.tight_layout()
plt.xlim(min(latlongs[:, 0]) - .0005, max(latlongs[:, 0]) + .0005)
plt.ylim(min(latlongs[:, 1]) - .0005, max(latlongs[:, 1]) + .0005)
plt.savefig(
    PATH + PLACE + str(CLST_METHOD) + ".png",
    dpi=250
)
plt.close()
##############################################################################
# Export distance matrix
##############################################################################
distPath = PATH + PLACE + "DIST.csv"
distMat = monet.calculateDistanceMatrix(latlongs, distFun=vn.vincenty) * 1000
np.savetxt(distPath, distMat.astype(int), fmt='%i', delimiter=',')
# heat = sns.heatmap(distMat, annot=False)
# heat.get_figure().savefig(PATH + PLACE + "DIST.png", dpi=500)
##############################################################################
# Export migration matrix
##############################################################################
migrPath = PATH + PLACE + "MIGR.csv"
zeroInflation = .72 ** .09
migrMat = monet.zeroInflatedExponentialMigrationKernel(
    distMat,
    params=monet.AEDES_EXP_PARAMS,
    zeroInflation=lifeStayProb ** adultMortality
)
monet.testMarkovMatrix(migrMat)
np.savetxt(migrPath, migrMat, delimiter=',')
# heat = sns.heatmap(migrMat, annot=False)
# heat.get_figure().savefig(PATH + "MIGR.png", dpi=500)