%matplotlib inline

import csv
import os
import glob
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import experimentsParser as exPar
plotly.tools.set_credentials_file(username='chipdelmal',api_key='wB4pF2t8VYoNC7iUrXSs')
offline.init_notebook_mode(connected=True)

# Define the experiment's path
dtype=float;
path="/Users/sanchez.hmsc/Desktop/ParserDataset/E_099_050_020_025";
aggregationDictionary=exPar.generateAggregationDictionary(["W","H","R","B"],[[0,0,1,2,3],[1,4,4,5,6],[2,5,7,7,8],[3,6,8,9,9]])

# Get the filenames lists
filenames=exPar.readExperimentFilenames(path)

# Load a single node (Auxiliary function)
nodeIndex=0
nodeData=exPar.loadNodeData(filenames.get("male")[nodeIndex],filenames.get("female")[nodeIndex],dataType=float)

# Aggregate the whole landscape into one array
landscapeSumData=exPar.sumLandscapePopulationsFromFiles(filenames,male=True,female=True,dataType=float)

# Aggregate the genotypes of a population (works for a node, or for all the population)
aggData=exPar.aggregateGenotypesInNode(landscapeSumData,aggregationDictionary)

# Load the population dynamics data of the whole landscape
landscapeData=exPar.loadLandscapeData(filenames,dataType=float)

# Aggregate node genotypes across all nodes
aggregationDictionary=exPar.generateAggregationDictionary(["W","H","R","B"],[[0,0,1,2,3],[1,4,4,5,6],[2,5,7,7,8],[3,6,8,9,9]])
aggregatedNodesData=exPar.aggregateGenotypesInLandscape(landscapeData,aggregationDictionary)


# plt.plot(aggData);

# Plot dynamics in a static plotly set
# tracesList=[]
# for i in range(0,len(columnsList)):
#     trace=go.Scatter(x=range(0,len(aggData)),y=aggData[:,i])
#     tracesList.append(trace)
# offline.iplot(tracesList, filename='basic-line')

labels=aggData["genotypes"]
colors=["rgb(25,128,255)","rgb(255,25,128)","rgb(128,0,255)","rgb(255,0,255)"]
inData=aggData["population"]
tracesList=[]
for i in range(0,len(labels)):
    trace=dict(
        x=range(0,len(inData)),
        y=inData[:,i],
        stackgroup='one',
        mode='lines',
        line=dict(width=3,color=colors[i]),
        name=labels[i]
    )
    tracesList.append(trace)
layout=go.Layout(
    title='Genotypes Breakdown',
    xaxis=dict(
        title='Time [days]',
        titlefont=dict(size=20,color='#7f7f7f')
    ),
    yaxis=dict(
        title='Allele Frequency',
        titlefont=dict(size=20,color='#7f7f7f')
    ),
    width=1000,
    height=350
)
fig=go.Figure(data=tracesList,layout=layout)
py.iplot(fig,filename='stacked-area-plot-hover',validate=False)



# x[:,2:]
# x[:, [1, 3]]
# columnsList=[[1,1],[1]]
# np.sum(x[:,columnsList[0]],axis=1)
