from graph_tool.all import *
import os, csv
import GFP
import NetSimilie
from pylab import *
from tabulate import tabulate

# Code for the experiment showing the sensativity to network size

def barabasiNetGen(size):

    g = price_network(size, m = 2, directed = False)
    return g

if __name__ == "__main__":
    finalR = []
    row = ["GraphSize", "GFPC-C", "GFPC-VC", "GFPC-GC", "NS"]
    finalR.append(row)
    resultFile = open('EXP1Results.txt', 'w')
    g = price_network(10000, m = 2, directed = False)

    g1 = Graph(g)
    graphSizes = [12800, 25600, 51200, 102400, 204800, 409600]
    graphs = []

    for i in graphSizes:
        g2 = barabasiNetGen(i)
        graphs.append(g2)

    count = 0
    # Loop through the generated graphs and compare with the source G
    for gp in graphs:
        vc, gc = GFP.GFPControl(g, gp)
        print("GFPC Result = ", (gc * 2) + vc, vc, gc)
        nsr = NetSimilie.netSimileControl(g, gp)
        print("NS Result = ", nsr)
        res = [count, ((gc * 2) + vc), vc, gc, nsr]
        count = count + 1
        finalR.append(res)

    resultFile.writelines(tabulate(finalR, headers="firstrow", tablefmt="grid"))
    resultFile.close()
