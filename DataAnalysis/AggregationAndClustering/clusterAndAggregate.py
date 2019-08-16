#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans


###############################################################################
# Parameters Setup
###############################################################################
(PATH, LATLONGS) = (
    "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/",
    "LandscapeOriginal/YorkeysKnob_01.csv"
)
(CLUSTERS_NO, REPS, SEED, JOBS) = (1000, 100, int(time.time()), 4)
(lifeStayProb, adultMortality) = (.72, .09)

###############################################################################
# Read latlongs
###############################################################################


###############################################################################
# Cluster
###############################################################################
clObj = KMeans(
    n_clusters=CLUSTERS_NO,
    random_state=SEED,
    n_jobs=JOBS
)
clustersObj = clObj.fit(latlongs)
(clusters, centroids) = (clustersObj.labels_, clustersObj.cluster_centers_)


###############################################################################
# Landscape aggregation
###############################################################################
