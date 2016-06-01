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

# Code for the experiment measuring the rumtime
if __name__ == "__main__":
    finalR = []
    row = ["GraphName", "GFPSingle", "GFPGlobal", "GFPTotal", "NetSimile"]
    finalR.append(row)
    resultFile = open('EXP3Results.txt', 'w')

    # Please put the directory of your SNAP files here
    for subdir, dirs, files in os.walk(""):
        for filename in files:
            g = Graph()
            edges = []
            filepath = subdir + os.sep + filename
            date =  datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            print date + ": " + filepath
            sys.stdout.flush()
            with open(filepath) as networkData:
                datareader = csv.reader(networkData, delimiter="	")
                for row in datareader:
                    edges.append([int(row[0]), int(row[1])])
            networkData.close()
            g.add_edge_list(edges, hashed=True) # Very important to hash the values here otherwise it creates too many nodes
            g.set_directed(False)


            for i in range(0, 5):
                NetTime = time.time()
                NetSimilie.netSimileSingleFingerprint(g)
                NetTime = time.time() - NetTime

                GFPSingle = time.time()
                GFP.GFPSingleFingerprint(g)
                GFPSingle = time.time() - GFPSingle

                GFPGlobal = time.time()
                GFP.globalFeatureExtraction(g)
                GFPGlobal = time.time() - GFPGlobal

                print NetTime, GFPSingle, GFPGlobal
                sys.stdout.flush()

                res = [filename, GFPSingle, GFPGlobal, (GFPSingle+GFPGlobal), NetTime]
                finalR.append(res)

                resultFile.writelines(tabulate(finalR, headers="firstrow", tablefmt="grid"))
                resultFile.flush()
        resultFile.close()
