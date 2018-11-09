import os
import csv
import fnmatch
import numpy as np
import experimentsParser as exPar

def writeFactorialAnalysisCSV(releasesNumber,coverage,path,experimentString,aggregateData,ratiosDictionary):
    # Getting common data for easier readability
    pop=aggregateData["population"]
    simDays=len(pop)
    numeratorList=ratiosDictionary["numerator"]
    denominatorList=ratiosDictionary["denominator"]
    #
    with open(path+experimentString+".csv", 'wb') as csvfile:
        writer=csv.writer(csvfile,delimiter=',')
        writer.writerow(["ReleasesNumber","Coverage","Day","Ratio"])
        for i in range(0,simDays):
            num=np.sum(pop[i,[numeratorList]])
            denom=np.sum(pop[i,[denominatorList]])
            ratio=num/denom
            writer.writerow([releasesNumber,coverage,i,ratio])
def splitExperimentString(experimentString):
    split=experimentString.split("_")
    releasesNumber=int(split[3])
    coverage=int(split[4])
    return {"releasesNumber":releasesNumber,"coverage":coverage}
def listDirectoriesInPath(path):
    file=os.listdir(path)
    folderNames=[name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name))]
    return folderNames
def loadFolderAndWriteFactorialCSV(experimentString,path,aggregationDictionary,ratiosDictionary,male=True,female=True,dataType=float):
    filenames=exPar.readExperimentFilenames(path+experimentString)
    landscapeSumData=exPar.sumLandscapePopulationsFromFiles(filenames,male=True,female=True,dataType=float)
    aggregateData=exPar.aggregateGenotypesInNode(landscapeSumData,aggregationDictionary)
    split=splitExperimentString(experimentString)
    writeFactorialAnalysisCSV(split["releasesNumber"],int(split["coverage"])/1000.0,path,experimentString,aggregateData,ratiosDictionary)
def compileFactorialCSVFromFiles(path,outFilename):
    filenames=[path+name for name in os.listdir(path) if fnmatch.fnmatch(name,'E_*.csv')]
    f=open(path+outFilename,'wb')
    for file in filenames:
        fileData=np.genfromtxt(file,skip_header=1,delimiter=",")
        np.savetxt(f,fileData,fmt='%2.5f',delimiter=",")
    f.close()
