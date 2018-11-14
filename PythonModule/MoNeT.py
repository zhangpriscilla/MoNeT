###############################################################################
# ╔╦╗┌─┐╔╗╔┌─┐╔╦╗
# ║║║│ │║║║├┤  ║
# ╩ ╩└─┘╝╚╝└─┘ ╩
# Mosquito Networks Taskforce
# Python module with network analysis routines
# Authors: Sarafina Smith, Biyonka Liang, Sabrina Wong, Héctor M. Sánchez C.
###############################################################################


###############################################################################
# Sabrina Wong, Sarafina Smith ################################################
###############################################################################
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
from matplotlib.colors import LinearSegmentedColormap

# Define 5 colormaps ranging from transparent to opaque.
cdict1 = {'red':   ((0.0, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 0.3, 0.3)),

         'alpha':((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),
        }

red1 = LinearSegmentedColormap('Red1', cdict1)

cdict2 = {'red':   ((0.0, 0.3, 0.3),
                   (1.0, 0.3, 0.3)),

         'green': ((0.0, 0.5, 0.5),
                   (1.0, 0.5, 0.5)),

         'blue':  ((0.0, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'alpha':((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),
        }

light_blue1 = LinearSegmentedColormap('LightBlue1', cdict2)


cdict3 = {'red':   ((0.0, 0.5, 0.5),
                   (1.0, 0.5, 0.5)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'alpha':((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),
        }

purple1 = LinearSegmentedColormap('Purple1', cdict3)


cdict4 = {'red':   ((0.0, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'alpha':((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),
        }

pink1 = LinearSegmentedColormap('Pink1', cdict4)

cdict5 = {'red':   ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 0.25, 0.25),
                   (1.0, 0.25, 0.25)),

         'blue':  ((0.0, 0.75, 0.75),
                   (1.0, 0.75, 0.75)),

         'alpha':((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),
        }

dark_blue1 = LinearSegmentedColormap('DarkBlue1', cdict5)
rgba_colors = [(1, 0, 0.3, 0.7), (1, 0, 1, 0.7), (0.5, 0, 1, 0.7), (0, 0.325, 0.75, 0.7)]

def colorClusterTrace(numClusters, clusterPoints):
    """
    Returns a trace to color each building according to its cluster id
    """
    colorTrace = [0] * numClusters
    col = 25
    for x in range(0, numClusters):
        colorTrace[x] = go.Scatter(
            x = clusterPoints[x][0],
            y = clusterPoints[x][1],
            name = 'Cluster ' + str(x) + ' Buildings',
            mode = 'markers',
            marker = dict(
                size = 6,
                color = 'rgba(' + str(col) + ',' + str(col) + ',' + str(col) + ', 0.75)',
            )
        )
        col += 25
        if col > 255:
            col -= 255
    return colorTrace

def clusterCenterTrace(clusterCenters, algorithmName):
    """
    Returns a trace of red cluster centers
    """
    return go.Scatter(
        x = clusterCenters[0],
        y = clusterCenters[1],
        name = algorithmName,
        mode = 'markers',
        marker = dict(
            size = 12,
            color = 'rgba(255, 0, 0, 0.75)'
            ,

        )
    )

def plot(colorTrace, centerTrace):
    #Plot result
    points = []
    for x in range(len(colorTrace)):
        points.append(colorTrace[x])
    points.append(centerTrace)
    #Gets name of city from the name of the csv file
    cityName = csvFileName.split("/")[1].split("_")[0]
    #Plot
    iplot({
            "data": points,
            'layout': {'title': cityName + ' Building Cluster Coordinates with ' + str(numClusters) + ' Clusters'}
            },
        )

def createClusterCenters(labels):
    """
    In: labels is a list of clusters generated by DBScan or AggClustering. labels[i] is the cluster id of buildings[i]
    Out: centersX is a list of x coordinates for each cluster center
         centersY is a list of y coordinates for each cluster center
         clusterPoints is a list of lists used for the trace where [i] is all x, y coords of buildings in cluster i
                    and clusterPoints[i][0] is a list of x values in cluster i and clusterPoints[i][1] is a list of y values in cluster i
    """
    points = [] #points is a list of lists where points[i] holds the coordinates of the buildings within cluster i

    clusterPoints = []

    #set up list of lists
    for x in range(0, len(labels)):
        points.append([])
        clusterPoints.append([])
        clusterPoints[x] = [[], []]

    #append each building to points based on its label
    for x in range(0, len(buildings)):
        if(labels[x] >= 0):
            points[labels[x]].append(buildings.as_matrix()[x])

    centersX = []
    centersY = []


    #find cluster center by averaging all points in each cluster
    for x in range(0, len(labels)):
        sumX = 0
        sumY = 0
        for y in range(0, len(points[x])):
            sumX += points[x][y][0]
            sumY += points[x][y][1]
            clusterPoints[x][0].append(points[x][y][0])
            clusterPoints[x][1].append(points[x][y][1])
        if(len(points[x]) > 0):
            centersX.append(sumX / len(points[x]))
            centersY.append(sumY / len(points[x]))

    return [centersX, centersY], clusterPoints, points

def euclideanDistance(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

def distBetweenCenters(centers):
    """
    In: list of tuples (x, y) of each cluster center
    Out: 2d array where array[i][j] is the distance between center i and center j
    """
    distances = []
    for i in range(len(centers)):
        distances.append([])
        for j in range(len(centers)):
            distances[i].append(euclideanDistance(centers[i], centers[j]))
    return distances

def minDistBetweenClusters(points):
    """
    In: points (computed in createClusterCenters), where points[i] is a list of tuples (x, y) of points in cluster i
    Out: 2d array where array[i][j] is the min distance between cluster i and cluster j
    """
    distances= []
    for i in range(len(points)):
        distances.append([])
        for j in range(len(points)):
            minDist = min([euclideanDistance(a, b) for a in points[i] for b in points[j]])
            distances[i].append(minDist)
    return distances

def maxDistBetweenClusters(points):
    """
    In: points (computed in createClusterCenters), where points[i] is a list of arrays [x, y] of points in cluster i
    Out: 2d array where array[i][j] is the min distance between cluster i and cluster j
    """
    distances= []
    for i in range(len(points)):
        distances.append([])
        for j in range(len(points)):
            allDistances = [euclideanDistance(a, b) for a in points[i] for b in points[j]]
            if(len(allDistances) > 0):
                print('ok')
                maxDist = max(allDistances)
                distances[i].append(maxDist)
            else:
                distances[i].append(None)
    return distances

def alleleCounts(csvFileName, columns, alleleNames, startCol = 3):
	"""
	In: columns is a list of lists describing the number of times each one indexed column should be counted for this allele
		eg [[1, 1, 2], [2, 3, 3]] if the given genotypes are WW, WR, and RR
		alleleNames is a list of the allele names for use as column titles eg ["W", "R"]
		startCol is the first column in the csv which lists genotypes, one indexed (column 1 in the columns argument)
	Out: A pandas dataframe with 1 column for each allele, containing the specified sum: eg  col 1 + col 1 + col 2 for "W"
    """
    # Love the idea of using the data type here to reduce memory use. We just need to have the option to make it float because
    #   the continuous time version of the model does allow "fractional" amounts of mosquitos.
    data = np.genfromtxt(csvFileName, dtype=int, skip_header=1, delimiter=",")
    res = df[['Time']]
    for i in range(len(columns)):
        # summed_col contains sum of counts for one allele, such as W
        summed_col = np.zeros_like(data[:,0])
        for index in columns[i]:
            # subtract 2 because index and start col are 1 indexed
            summed_col += data[:,index+startCol - 2]
        allele = alleleNames[i]
        res.insert(i + startCol - 1, alleleNames[i], summed_col)
    return res

def allCounts(csvPath, columns, alleleNames, female=True):
	"""
	In: csvPath is a folder of CSV files, such as "CRISPR_SIT/"
		columns is a list of lists describing the number of times each one indexed column should be counted for this allele
		eg [[1, 1, 2], [2, 3, 3]] if the given genotypes are WW, WR, and RR
		alleleNames is a list of the alleleNames. One dataframe is made for each.
		female specifies whether to count male or female mosquitoes
	Out: List of data frames with one allele count column for each run of that gender
		 eg  W1W2...WnW1W2...Wn  representing the count of W over n experiments on female mosquitoes
	"""
    if female:
        files = glob.glob(csvPath + 'AF1*.csv')
    else:
        files = glob.glob(csvPath + 'ADM*.csv')
    res = [df[['Time']] for _ in range(len(alleleNames))]
    for i in range(len(files)):
        count_df = alleleCounts(files[i], columns, alleleNames, 2)
        for j in range(len(alleleNames)):
            res[j].insert(i + 1, alleleNames[j] + str(i), (count_df[alleleNames[j]]).copy())
    for j in range(len(alleleNames)):
        res[j] = res[j].set_index("Time").T
    return res

def makeAlleleCountPlot(alleleCounts, title, linewidth, opacity, color):
	# alleleCounts is table outputted by allCounts
    alleleCounts.plot(x="Time", figsize=(15, 5), linewidth = linewidth, legend=False, title = title, color = color, alpha = opacity)
    plt.ylabel("Allele Count")
    plt.show()

def plotIndividualAlleles(csvPath, columns, alleleNames, female=True):
	"""
	In:  csvPath is a folder of CSV files, such as "CRISPR_SIT/"
		columns is a list of lists describing the number of times each one indexed column should be counted for this allele
		eg [[1, 1, 2], [2, 3, 3]] if the given genotypes are WW, WR, and RR
		alleleNames is a list of the alleleNames.
		female specifies whether to count male or female mosquitoes
	Out: Plot a heatmap of each allele over time. One horizontal line in the heatmap represents one patch's alleles
		 over time with the opacity of the line defined by the allele count.
		 The overall map comes from stacked horizontal lines, one from each csv file.
	"""
	cmaps = [light_blue1, red1, purple1, pink1]
	counts = allCounts(csvPath, columns, alleleNames, female)
	for i in range(len(alleleNames)):
	    fig, ax = plt.subplots(figsize=(20, 5))
	    ax.set_ylabel(alleleNames[i])
	    im = ax.imshow(counts[i], cmap=cmaps[i])

def plotAllAlleles(csvPath, columns, alleleNames, female=True):
	# overlay all allele heatmaps such as those produced by plotIndividualAlleles
    cmaps = [light_blue1, red1, purple1, pink1]
    counts = allCounts(csvPath, columns, alleleNames, female)
    fig = plt.figure(figsize=(20, 5))
    for i in range(len(alleleNames)):
        plt.imshow(counts[i], cmap=cmaps[i])

def stackedAreaPlot(csvPath, columns, alleleNames, female=True):
	#stacks the total count of each alele over time, summed over all nodes.
    counts = allCounts(csvPath, columns, alleleNames, female)
    allele_dict = {}
    for i in range(len(alleleNames)):
        allele_dict[alleleNames[i]] = counts[i].sum()
    res = pd.DataFrame(allele_dict)
    return res.plot.area(color=rgba_colors)

def exportStackedAreaPlots(csvPath, columns, alleleNames, female=True):
	"""
	In: csvPath is a folder with folders of CSV files and an images folder.
	Out: For each folder of CSV files, put a stacked area plot in the images folder.
	     Each plot stacks the total count of each allele over time, summed over all nodes in the folder.
	"""
    folders = glob.glob(csvPath + '*/')

    for f in folders:
        plot = stackedAreaPlot(f, columns, alleleNames, female)
        fig = plot.get_figure()
        fig.savefig(csvPath + '/images/' + f.split(csvPath)[1][:-1])
        plt.close(fig)

################################################################################
############################### Biyonka Liang ##################################
################################################################################

def out_transition_freq(n, matrix, community):
    #start = time.time()
    out = []
    nodes = np.arange(n)
    for i in nodes:
        if i not in community:
            out.append(i)
    ixgrid = np.ix_(community, out)
    m = matrix[ixgrid]
    #end = time.time()
    return m.sum()

def within_transitions(matrix, community):
    ixgrid = np.ix_(community, community)
    m = matrix[ixgrid]
    s = m.sum()
    return s

def out_transitions(matrix, community):
    within = within_transitions(matrix, community)

    #start = time.time()
    ixgrid = np.ix_(community)
    m = matrix[ixgrid, :]
    out_transitions = m.sum()
    #end = time.time()
    return out_transitions - within

def in_transitions(matrix, community):
    within = within_transitions(matrix, community)

    ixgrid = np.ix_(community)
    m_in = matrix[:, ixgrid]
    in_transitions = m_in.sum()
    return in_transitions - within

def ratio(matrix, community):
    o = out_transitions(matrix, community)
    i = in_transitions(matrix, community)
    return i/o

def classify(ratio, bounds):
    '''bounds = [upper bound for source, lower bound for sink]'''
    if ratio < bounds[0]:
        return "sink"
    elif ratio > bounds[1]:
        return "source"
    else:
        return "manager"

def get_transition_freq(matrix, community):
    '''matrix is a numpy matrix describing the transition matrix for a graph. communities is a list of nodes'''
    #A_{ij}: represents frequency of transition from node i to node j

    #sums entries of square matrix that represents all transitions within the community and from community outward
    #np.ix_ allows easier subsetting by creating n-d meshgrid for the matrix
    ixgrid = np.ix_(community)
    m = matrix[ixgrid, :]
    comm_out_transitions = m.sum()

    m_in = matrix[:, ixgrid]
    comm_in_transitions = m_in.sum()

    #sums entries of square matrix that represents all transitions within the community only
    ixgrid_c = np.ix_(community, community)
    m_c = matrix[ixgrid_c]
    within_transition = m_c.sum()

    #subtract total community transitions from within community transitions
    out_transition = comm_out_transitions - within_transition
    in_transition = comm_in_transitions - within_transition

    ratio = in_transition/out_transition
    return (in_transition, out_transition, ratio)
