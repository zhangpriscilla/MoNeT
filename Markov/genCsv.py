import genSingleCsv as gS

###############################################################################
# Main
###############################################################################
# Define sim parameters
(reps, n, zeroInflation) = (500, [5 ** 2], .75)
mskMat = [
        [0.30, 0.70, 0.00],
        [0.70, 0.30, 0.00],
        [0.00, 0.00, 1.00]
    ]

# Generate landscapes with two point-types and different probabilities
probsList = [.999, .500]
for pA in probsList:
    gS.genCSV(reps, n, [0], [[pA, 1-pA, 0.0]], mskMat, zeroInflation)
