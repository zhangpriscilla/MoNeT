import matplotlib.pyplot as plt

def plotNodeDataRepetitions(
    nodeRepetitionsArray,
    style,
    xCord,
    yRange
):
    """
    Description:
        * Generates the "traces" plot for one node.
    In:
        * nodeRepetitionsArray: Intermediate structure generated by taking
            the information of a given node accross all landscapes.
        * style: styling options for the plot
    Out:
        * fig: matplotlib traces figure
    Notes:
        * This function is meant to work within plotLandscapeDataRepetitions,
            so it's not necessary to call it directly.
    """
    probeNode = nodeRepetitionsArray
    repsNumber = len(probeNode)
    genesNumber = len(probeNode[0][0])
    fig, ax = plt.subplots()
    ax.set_aspect(aspect=style["aspect"])
    for j in range(0, repsNumber):
        transposed = probeNode[j].T
        for gene in range(0, genesNumber):
            ax.plot(
                transposed[gene],
                linewidth=style["width"],
                color=style["colors"][gene],
                alpha=style["alpha"]
            )
    ax.plot([xCord, xCord], [0, yRange], 'k--', lw=.25)
    return fig


def plotLandscapeDataRepetitions(
    landscapeReps,
    style,
    xCord,
    yRange
):
    """
    Description:
        * Generates the individual "traces" plots for a whole landscape.
    In:
        * landscapeReps: landscape repetitions data generated with
            loadAndAggregateLandscapeDataRepetitions.
        * style: styling options for the plot.
    Out:
        * figs: array of matplotlib traces figures.
    Notes:
        * NA
    """
    landscapes = landscapeReps["landscapes"]
    landscapesNumb = len(landscapeReps["landscapes"][0])
    figs = [None] * landscapesNumb
    for i in range(0, landscapesNumb):
        probeNode = zip(*landscapes)[i]
        figs[i] = plotNodeDataRepetitions(probeNode, style, xCord, yRange)
    return figs
