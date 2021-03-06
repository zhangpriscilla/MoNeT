
import MoNeT_MGDrivE as monet
import auxiliaryFunctions as aux

###############################################################################
# Select experiment & output setup
###############################################################################
BATCH = True
DRIVE = 4
EXPORT_TO_DRIVE = True
PROBED = "E_85_50_20_50"
# Key: E_(Cutting rate)_(H allele cost)_(releases)_(mosquitoes per release)
###############################################################################
# Setup variables
###############################################################################
id, aggregationDictionary = aux.driveSelector(DRIVE)
path = "/Volumes/marshallShare/CLEAVR/"+id+"/ANALYZED/"
if EXPORT_TO_DRIVE:
    output = "/Volumes/marshallShare/CLEAVR/"+id+"/images/"
else:
    output = "./images/"+id+"/"
directories = monet.listDirectoriesWithPathWithinAPath(path)
# Style .......................................................................
colors = ["#090446", "#ed0091", "#7fff3a", "#7692ff", "#29339b", "#c6d8ff"]
if (DRIVE == 1) or (DRIVE == 2):
    aspect, yrange = [.0175, 50000]
elif (DRIVE == 3) or (DRIVE == 4):
    aspect, yrange = [.0175, 50000]
styleTrace = {
    "width": 2, "alpha": 1, "dpi": 512, "legend": True,
    "aspect": aspect, "colors": colors, "xrange": 3600, "yrange": yrange
}
styleStack = {
    "width": 0, "alpha": .95, "dpi": 512, "legend": True,
    "aspect": aspect, "colors": colors, "xrange": 3600, "yrange": yrange
}
###############################################################################
# Run Routine
###############################################################################
if BATCH is False:
    experimentString = PROBED
    aggData = aux.aggregateDataFromPath(
        path+experimentString, aggregationDictionary
    )
    # aux.exportMeanPlotToDirectory(
    #     output+experimentString, aggData, styleTrace
    # )
    aux.exportStackedPlotToDirectory(
        output+experimentString, aggData, styleStack
    )
else:
    for i in range(0, len(directories)):
        experimentString = directories[i].split("/")[-1]
        aggData = aux.aggregateDataFromPath(
            path+experimentString, aggregationDictionary
        )
        # aux.exportMeanPlotToDirectory(
        #     output+experimentString, aggData, styleTrace
        # )
        aux.exportStackedPlotToDirectory(
            output+experimentString, aggData, styleStack
        )
