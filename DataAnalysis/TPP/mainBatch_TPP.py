import plotly #NOTE: needs dev version of plotly (because of 'stackgroup')
import plotly.graph_objs as go
import plotly.offline as offline
import plotly.io as pio
import MoNeT_MGDrivE as monet
import plotly.plotly as py
import os
offline.init_notebook_mode(connected=True)

###############################################################################
# MCR Construct
###############################################################################

# Define the experiment's path, aggregation dictionary, and read filenames
type = float
path = "/Volumes/marshallShare/TPP/SplitDrive/ANALYZED/"
directories=monet.listDirectoriesWithPathWithinAPath(path)

aggData

#------------------------------------------------------------------------------
# Data Handling
#------------------------------------------------------------------------------
for i in range(0,len(directories)):
    experimentString=directories[i].split("/")[-1]
    # aggregationDictionary = monet.generateAggregationDictionary(
    #     ["W", "H", "R", "B"],
    #     [
    #         [0, 0, 1, 2, 3],
    #         [1, 4, 4, 5, 6],
    #         [2, 5, 7, 7, 8],
    #         [3, 6, 8, 9, 9]
    #     ]
    # )
    filenames = monet.readExperimentFilenames(path + experimentString)

    # To analyze the sum of the whole landscape ..................................
    # Sum landscape into one array ("in place" memory-wise)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames,
        male=True,
        female=True,
        dataType=float
    )
    aggregationDictionary=monet.autoGenerateGenotypesDictionary(
        ["W","H","R","B"],
        landscapeSumData["genotypes"]
    )
    # Aggregate genotypes (node or landscape) ....................................
    aggData = monet.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )

    #------------------------------------------------------------------------------
    # Plotting
    #------------------------------------------------------------------------------

    labels = aggData["genotypes"]
    colors = ["rgb(25,128,255)", "rgb(255,25,128)",
              "rgb(128,0,255)", "rgb(255,0,255)"]
    inData = aggData["population"]

    # Plot allele frequency dynamics .............................................
    tracesList = []
    for i in range(0, len(labels)):
        trace = dict(
            x=range(0, len(inData)),
            y=inData[:, i],
            stackgroup='one',
            mode='lines',
            line=dict(width=3, color=colors[i]),
            name=labels[i]
        )
        tracesList.append(trace)
    layout = go.Layout(
        title='Genotypes Breakdown',
        xaxis=dict(
            title='Time [days]',
            titlefont=dict(size=20, color='#7f7f7f')
        ),
        yaxis=dict(
            title='Allele Frequency',
            titlefont=dict(size=20, color='#7f7f7f')
        ),
        width=1500,
        height=400
    )
    fig = go.Figure(data=go.Data(tracesList), layout=layout)
    #py.iplot(fig,filename='stacked-area-plot-hover',validate=False)
    plotly.offline.plot(
        fig,
        filename=("./images/"+experimentString+'_frequency.html'),
        auto_open=False
    )


    # Plot allele ratio dynamics ..................................................
    tracesList = []
    for i in range(0, len(labels)):
        trace = dict(
            x=range(0, len(inData)),
            y=inData[:, i],
            stackgroup='one',
            groupnorm='fraction',
            mode='lines',
            line=dict(width=3, color=colors[i]),
            name=labels[i]
        )
        tracesList.append(trace)
    layout = go.Layout(
        title='Genotypes Breakdown',
        xaxis=dict(
            title='Time [days]',
            titlefont=dict(size=20, color='#7f7f7f')
        ),
        yaxis=dict(
            title='Allele Ratio',
            titlefont=dict(size=20, color='#7f7f7f')
        ),
        width=1500,
        height=400
    )
    fig = dict(data=tracesList, layout=layout)
    plotly.offline.plot(
        fig,
        filename=("./images/"+experimentString+'_ratio.html'),
        auto_open=False
    )
