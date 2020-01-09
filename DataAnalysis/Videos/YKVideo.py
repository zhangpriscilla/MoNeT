###############################################################################
# Clustered video routines
###############################################################################
#   In case of:
#       UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1
#       https://github.com/matplotlib/basemap/issues/324
###############################################################################
import aux
import subprocess
import MoNeT_MGDrivE as monet

###############################################################################
# Colors and genotypes
###############################################################################
colors = [
        "#090446", "#f20060", "#ff28d4", "#7fff3a", "#c6d8ff", '#6e44ff',
        '#e56399', '#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta',
        'purple', 'black', 'cyan', 'teal'
    ]
groups = ["W", "H", "R", "B", "E"]

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
BASE_PATH = '/Volumes/marshallShare/ERACR/Yorkeys4/'
expFolder = BASE_PATH + 'Experiment4/Yorkeys_AGG_1_00001'
extras = BASE_PATH + '/Yorkeys4/Clustered/'
expPath = expFolder + '/ANALYZED/' + 'E_0200_30_20_02_00020'

###############################################################################
# File names parsing
###############################################################################
(patchFilePattern, imagePattern) = (
        {'males': '/M_*', 'females': '/F_*'},
        '/c_%06d.png'
    )
expBaseName = expFolder.split('/')[-1]
(clusteringNum, bgName, originalCoordFile) = (
        int(expBaseName.split('_')[-1]),
        expBaseName.replace('_AGG_', '_VBG_'),
        extras + expBaseName.replace('_AGG_', '_CLS_') + '.csv'
    )
(clusterName, background, vname, imageLocation) = (
        bgName.replace('VBG_', 'AGCV_'),
        extras + bgName + '.png',
        expPath.replace('ANALYZED', 'videos') + '.mp4',
        expPath.replace('ANALYZED', 'images/clustercharts')
    )
original_corners = aux.get_corners(originalCoordFile)
coordinates = monet.getClusters(extras+clusterName+'.csv')

###############################################################################
# Create video
###############################################################################
subprocess.Popen(['mkdir', imageLocation])
clusters = monet.populateClusters(
        len(coordinates[0]), '', expPath, patchFilePattern
    )
genotypes = monet.getGenotypes(clusters[0]['male'][0])
aggDict = monet.autoGenerateGenotypesDictionary(groups, genotypes)
aggList = monet.aggregateClusters(clusters, aggDict)
monet.generateClusterGraphs(
        aggList, coordinates, imageLocation, colors, original_corners,
        0.002, 512, skip=True
    )
video = monet.generateVideo(vname, background, imageLocation, imagePattern)
video.wait()
