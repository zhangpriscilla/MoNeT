import glob
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

colors = ['red','blue','green','yellow','magenta','purple', 'black', 'cyan', 'teal']
def draw_pie(ax,ratios, X=0, Y=0, radius=300):
    N = len(ratios)
    xy = []
    start = 0.
    for ratio in ratios:
        x = [0] + np.cos(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        y = [0] + np.sin(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        xy1 = zip(x,y)
        xy.append(xy1)
        start += ratio

    for i, xyi in enumerate(xy):
        ax.scatter([X],[Y] , marker=(xyi,0), s=radius)

def getCoordinates(fileLocation):
    patchFile = open(fileLocation,"r")
    patchesX = []
    patchesY = []
    for line in patchFile:
        coordinates = line.split(',')
        patchesX.append(float(coordinates[0]))
        patchesY.append(float(coordinates[1]))
    patchFile.close()
    return(patchesX,patchesY)

def getSizes(fileLocation):
    populationFile = open(fileLocation,"r")
    radiuses = []
    for line in populationFile:
        radiuses.append((math.log(float(line))**2)*0.8)
    populationFile.close()
    return radiuses

def getRatios(populations, groups, weights):
    groupPopulation= []
    total = 0
    for i in range(len(groups)):
        population = 0
        for j in range(len(groups[i])):
            population+= (populations[(groups[i][j])-1]*weights[i][j])
        total+= population
        groupPopulation.append(population)
    ratios = [float(pop)/total for pop in groupPopulation]
    return ratios

def main():
    coordinateFileLocation = raw_input("Coordinate file location?\n")
    #"/Users/vferman/Downloads/Madagascar/Madagascar_Coordinates.csv"
    patchesX,patchesY = getCoordinates(coordinateFileLocation)
    #"/Users/vferman/Downloads/Madagascar/Madagascar_Populations.csv"
    popFileLocation = raw_input("Population file location?\n")
    radiuses = getSizes(popFileLocation)

    clases=int(raw_input("Number of different populations?\n"))
    groups=int(raw_input("How many groups would you like?\n"))
    if(groups==0 or groups==1):
        groups=clases
        columsToGroup=[]
        columnsWeight=[]
        for i in range(0,clases):
            columsToGroup.append([i])
            columnsWeight.append([1])
    else:
        columsToGroup=[]
        columnsWeight=[]
        for i in groups:
            groupN = raw_input("Which populations should we group in group"+ str(i+1) +"(i.e. 1,3,5)?\n")
            cols = groupN.split(',')
            columsToGroup.append([int(elem) for elem in cols])
            weights = [0]*len(cols)
            for j,col in enumerate(cols):
                colW =raw_input("How should we weight the contents of colum"+ col +"(0 means it should be ignored)?\n")
                weights[j]=colW
            columnsWeight.append(weights)

    dataFileLocation=raw_input("Where are the files located?\n")
    #"/Users/vferman/Downloads/Madagascar/Replacement_D/0001/AF1_Aggregate_Run1_*.csv"
    fileNames = sorted(glob.glob(dataFileLocation))
    files =[]
    lineCount = len(open(fileNames[0]).readlines())-1
    for fileName in fileNames:
        files.append(open(fileName,'r'))

    #pieMatrix =[]
    patches=len(files)
    for f in files:
        next(f)

    for i in range(lineCount):
        fig, ax = plt.subplots()

        for patch in range(0,patches):
            line = next(files[patch]).split(',')
            sizes = [float(elem) for elem in line]
            sizes = sizes[1:]
            ratios = getRatios(sizes, columsToGroup, columnsWeight)
            draw_pie(ax,ratios,patchesY[patch],patchesX[patch],radiuses[patch])

        plt.show()
        plt.savefig(str(i)+"-"+str(groups)+".png", dpi=461,
                facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=False, bbox_inches=None, pad_inches=0.05,
                frameon=None)
        plt.close(fig)
        plt.close('all')

    for f in files:
        f.close()


main()
