from graph_tool.all import *
import os, csv, time, datetime, sys
import GFP
import NetSimilie
from pylab import *
from tabulate import tabulate

# Code for the experiment measuring the rumtime of the code
if __name__ == "__main__":
    finalR = []
    row = ["GraphName", "GFPSingle", "GFPGlobal", "GFPTotal", "NetSimile"]
    finalR.append(row)
    resultFile = open('EXP3Results.txt', 'w')

    #for subdir, dirs, files in os.walk("/home/lzdh59/NetworkData"):
    for subdir, dirs, files in os.walk("/Volumes/Share_Drive/NetworkData/LCCT/"):
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
