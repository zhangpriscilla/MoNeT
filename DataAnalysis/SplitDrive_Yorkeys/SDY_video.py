#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Clustered video routines
###############################################################################
# In case of:
#   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1
#   https://github.com/matplotlib/basemap/issues/324
#       replace all "utf-8" with "latin-1" in shapefile.py, which located in
#       ~/Library/Python/3.7/lib/python/site-packages/shapefile.py
# Depends on an obsolete structure (needs to be updated):
#   https://github.com/Chipdelmal/MoNeT/blob/master/DataAnalysis/ERACR/Yorkeys.py
#   https://github.com/Chipdelmal/MoNeT/tree/master/DataAnalysis/AggregationAndClustering
###############################################################################
import sys
import glob
import warnings
import datetime
import SDY_aux as aux
import SDY_select as sel
import MoNeT_MGDrivE as monet
warnings.filterwarnings("ignore", category=UserWarning)


(BASE_PATH, fldName, kernelName) = (
        '/RAID5/marshallShare/SplitDrive_Yorkeys/',
        sys.argv[1], sys.argv[2]

    )
DATA_PATH = '/RAID5/marshallShare/SplitDrive_Yorkeys/{}/{}/'.format(
        fldName, kernelName
    )
(dataFldr, expName, clstFldr, aggLvl, clstSample) = (
        'geoProof', 'Aggregated', 'clustered', 'C000100', '0000'
    )
(PAD, DPI) = (.1, 512)
###############################################################################
# Colors and genotypes
###############################################################################
colors = ['#090446', '#ff004d', '#7fff3a', '#9037dd', '#ffed38']
(_, aggDict, _, _) = sel.driveSelector(1, False, '')
###############################################################################
# File paths
###############################################################################
#   BASE_PATH: Root directory for the experiment
#   expFolder: Folder that contains the [ANALYZED, GARBAGE, RAW] sets
#   extras: Folder that contains the [MAP, VBG, CLS, CLL, AGG, AGCV] files
#       generated by the aggregation routines
#   expPath: Folder nested within the ANALYZED folder for parameters sweeps
#       (would be equal to expFolder in case it's not existing)
###############################################################################
(extras, expPath, outPath) = (
        '{}{}/'.format(BASE_PATH, clstFldr),
        '{}/ANALYZED/0001/'.format(DATA_PATH),
        '{}video/{}/'.format(BASE_PATH, kernelName)
    )
monet.makeFolder(outPath)
###############################################################################
# File names parsing
###############################################################################
#   VBG: Clustered PNG
#   CLL: Number of nodes in cluster?
#   CLS: {x, y, clusterID} -> contained now in "_I"
#   AGG: Aggregated migration matrix "_A"
#   AGCV: Clusters centroids? -> contained now in "_I"
###############################################################################
(patchFilePattern, imagePattern) = (
        {'male': '/M_*', 'female': '/F_*'}, 'c_%06d.png'
    )
(bgName, originalCoordFile) = (
        glob.glob(extras + aggLvl + '_' + clstSample + '*VBG.png')[0],
        glob.glob(extras + aggLvl + '_' + clstSample + '*I.csv')[0]
    )
(imgLocation, videoLocation) = (
        outPath,
        '{}video/{}.mp4'.format(BASE_PATH, kernelName)
    )
original_corners = monet.get_corners(originalCoordFile)
(coordinates, clstList) = (
        monet.getClustersFromAggFiles(originalCoordFile),
        monet.readClustersIDs(originalCoordFile)
    )
###############################################################################
# Terminal message
###############################################################################
print(aux.PAD)
print('{}Exporting video [{}]{}'.format(
            aux.CWHT, str(datetime.datetime.now()), aux.CEND
        ))
print(aux.PADL + aux.CRED)
print('* PATH base: \t{}'.format(BASE_PATH))
print('* PATH data: \t{}'.format(DATA_PATH))
print('* PATH imgs: \t{}'.format(imgLocation))
print('* PATH video: \t{}'.format(videoLocation))
print(aux.CEND + aux.PADL)
###############################################################################
# Export Frames
###############################################################################
clusters = monet.populateClustersFromList(clstList, expPath, patchFilePattern)
aggList = monet.aggregateClusters(clusters, aggDict)
ticks = aggList[0].shape[0]
monet.generateClusterGraphs(
        originalCoordFile,
        aggList, coordinates, imgLocation, colors, original_corners,
        PAD, DPI, skip=False, countries=True, refPopSize=1500
    )
print('* Finished exporting frames ({}/{})'.format(ticks, ticks))
print('* Please run the following command in the terminal:')
###############################################################################
# Generate video
###############################################################################
console = [
            'ffmpeg',
            '-r', '30',
            '-f', 'image2',
            '-s', '4096x2160',
            '-i', '{}c_%06d.png'.format(imgLocation),
            '-vf', '"pad=ceil(iw/2)*2:ceil(ih/2)*2"',
            '-vcodec', 'libx264',
            '-crf', '25',
            '-pix_fmt', 'yuv420p', videoLocation
        ]
# video = subprocess.Popen(console)
# video.wait()
###############################################################################
# Terminal message
###############################################################################
print(aux.CWHT + ' '.join(console) + aux.CEND)
print(aux.PADL)
print('{}Exported frames [{}]{}'.format(
            aux.CWHT, str(datetime.datetime.now()), aux.CEND
        ))
print(aux.PAD)
