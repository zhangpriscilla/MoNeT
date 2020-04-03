#!/usr/bin/python
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
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
# Example of use:  python SDY_video.py 'dsk' 'E_30_30_100'
###############################################################################
import sys
import glob
import datetime
import subprocess
import SDY_aux as aux
import SDY_functions as fun
import SDY_select as sel
import MoNeT_MGDrivE as monet

# Aggregated: Selective
# unAggregated: Uniformly
if sys.argv[1] == 'srv':
    VOL = '/RAID5/marshallShare/'
else:
    VOL = '/home/chipdelmal/Desktop/'
HLT = True
###############################################################################
# Paths
###############################################################################
(BASE_PATH, fldName, expName, clstType, kernelName) = (
        '{}SplitDrive_Yorkeys'.format(VOL),
        'geoProof', 'Aggregated', 'Selective', sys.argv[2]
        # 'E_30_30_100'
        # sys.argv[1], sys.argv[2]
    )
DATA_PATH = '{}/{}/{}'.format(BASE_PATH, fldName, expName)
(dataFldr, clstFldr, aggLvl, clstSample) = (
        fldName,
        'Landscapes/LandAggregated/{}/'.format(clstType),
        'C000893', '0001'
    )
(PAD, DPI) = (.001, 512)
###############################################################################
# Colors and genotypes
###############################################################################
(_, aggDict, colors, _) = sel.driveSelectorVideo(1, HLT, '')
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
        '{}/{}/'.format(BASE_PATH, clstFldr),
        '{}/ANALYZED/{}/'.format(DATA_PATH, kernelName),
        '{}/video/{}/{}/'.format(BASE_PATH, expName, kernelName)
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
        glob.glob(extras+aggLvl+'/Yorkeys01_'+clstSample+'*_VBG.png')[0],
        glob.glob(extras+aggLvl+'/Yorkeys01_'+clstSample+'*_I.csv')[0]
    )
(imgLocation, videoLocation) = (
        outPath, '{}/video/{}/{}.mp4'.format(BASE_PATH, expName, kernelName)
    )
original_corners = monet.get_corners(originalCoordFile)
(coordinates, clstList) = (
        monet.getClustersFromAggFiles(originalCoordFile),
        monet.readClustersIDs(originalCoordFile)
    )
###############################################################################
# Terminal message
###############################################################################
print(aux.PADA)
print('{}Exporting video [{}]{}'.format(
            aux.CWHT, str(datetime.datetime.now()), aux.CEND
        ))
print(aux.PADB + aux.CRED)
print('* PATH base: \t{}'.format(BASE_PATH))
print('* PATH data: \t{}'.format(DATA_PATH))
print('* PATH expr: \t{}'.format(expPath))
print('* PATH video: \t{}'.format(videoLocation))
print(aux.CEND + aux.PADB)
###############################################################################
# Export Frames
###############################################################################
print(expPath)
print('* Populating clusters list', end='\r')
clusters = monet.populateClustersFromList(clstList, expPath, patchFilePattern)
print('* Populating aggregations list', end='\r')
aggList = monet.aggregateClusters(clusters, aggDict)
print('* Generating videos frames to folder')
ticks = aggList[0].shape[0]
fun.generateClusterGraphs(
        originalCoordFile,
        aggList, coordinates, imgLocation, colors, original_corners,
        PAD, DPI, skip=False, countries=False, refPopSize=2
    )
print('* Finished exporting frames ({}/{})'.format(ticks, ticks))
print('* Please run the following command in the terminal:')
###############################################################################
# Generate video
###############################################################################
console = [
            'ffmpeg', '-y', '-r', '30', '-f', 'image2', '-s', '4096x2160',
            '-i', '{}c_%06d.png'.format(imgLocation),
            '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-vcodec', 'libx264',
            '-crf', '25', '-pix_fmt', 'yuv420p', videoLocation
        ]
video = subprocess.Popen(console)
video.wait()
###############################################################################
# Terminal message
###############################################################################
print(aux.CWHT + ' '.join(console) + aux.CEND)
print(aux.PADB)
print('{}Exported frames [{}]{}'.format(
            aux.CWHT, str(datetime.datetime.now()), aux.CEND
        ))
print(aux.PADA)
