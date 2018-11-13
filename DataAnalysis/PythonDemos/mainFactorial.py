import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from sklearn.externals.joblib import Parallel, delayed
import time
import MoNeT_MGDrivE as monet

###############################################################################
# Factorial Experiment Example
###############################################################################
path = "/Users/sanchez.hmsc/Desktop/2018_11_06_ANALYZED/"
wildsList = [1, 1, 2, 2, 3, 3, 4, 5, 6, 1, 1, 2, 4, 4, 5, 7, 7, 8]
homingList = [4, 5, 6, 7, 7, 8, 8, 9, 9, 2, 3, 3, 5, 6, 6, 8, 9, 9]
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H"],
    [
        [x - 1 for x in wildsList],
        [x - 1 for x in homingList]
    ]
)
ratiosDictionary = {
    "numerator": [1],
    "denominator": [0, 1]
}

###############################################################################
# Export Individual CSVs for Factorial Slots
###############################################################################
# experimentFolders=fac.listDirectoriesInPath(path)
# for folder in experimentFolders:
#     fac.loadFolderAndWriteFactorialCSV(folder,path,aggregationDictionary,ratiosDictionary)
start = time.time()
experimentFolders = monet.listDirectoriesInPath(path)
Parallel(n_jobs=4)(delayed(
    monet.loadFolderAndWriteFactorialCSV)(
        experimentString=folder,
        path=path,
        aggregationDictionary=aggregationDictionary,
        ratiosDictionary=ratiosDictionary
    )
    for folder in experimentFolders
)
end = time.time()
print(end - start)
###############################################################################
# Load and Compile CSVs into one
###############################################################################
outFilename = "A_FlattenedFactorial.csv"
monet.compileFactorialCSVFromFiles(path, outFilename)
