from graph_tool.all import *
import os, csv, time, datetime, sys
import GFP
import NetSimilie
from pylab import *
from tabulate import tabulate

def barabasiNetGen(size):

    g = price_network(size, m = 2, directed = False)
    return g

# Code for the experiment measuring the rumtime of the code
if __name__ == "__main__":
    finalR = []
    row = ["GraphName", "GFPSingle", "GFPGlobal", "GFPTotal", "NetSimile"]
    finalR.append(row)
    resultFile = open('EXP4Results.txt', 'w')

    graphSizes = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
    graphs = []
    count  = 0
    for i in graphSizes:
        g = barabasiNetGen(i)
        graphs.append(g)

    for g in graphs:
        for i in range(0, 5):
            print graphSizes[count]

            GFPSingle = time.time()
            GFP.GFPSingleFingerprint(g)
            GFPSingle = time.time() - GFPSingle

            GFPGlobal = time.time()
            GFP.globalFeatureExtraction(g)
            GFPGlobal = time.time() - GFPGlobal

            print GFPSingle, GFPGlobal
            sys.stdout.flush()

            res = [graphSizes[count], GFPSingle, GFPGlobal, (GFPSingle+GFPGlobal)]
            finalR.append(res)

            resultFile.writelines(tabulate(finalR, headers="firstrow", tablefmt="grid"))
            resultFile.flush()
        count = count + 1
    resultFile.close()
