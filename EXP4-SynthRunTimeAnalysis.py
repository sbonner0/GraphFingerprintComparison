# Writen by Stephen Bonner 2016
#This file is part of GraphFingerprintComparison.

#GraphFingerprintComparison is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#GraphFingerprintComparison is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with GraphFingerprintComparison.  If not, see <http://www.gnu.org/licenses/>.
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
