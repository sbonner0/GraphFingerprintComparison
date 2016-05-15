from graph_tool.all import *
import os, csv
import GFP
import NetSimilie
from pylab import *
from tabulate import tabulate

# Code for the experiment showing the sensativity to network topology

def printDegreeDist(g, name):
    # Plot the degree distribution of the passed graph
    total_hist = vertex_hist(g, "total")
    y = total_hist[0]
    figure(figsize=(6,4))
    errorbar(total_hist[1][:-1], total_hist[0], fmt="o", label="total")
    gca().set_yscale("log")
    gca().set_xscale("log")
    subplots_adjust(left=0.2, bottom=0.2)
    xlabel("$k_{total}$")
    ylabel("$NP(k_{total})$")
    #tight_layout()
    savefig(name)

def randomRewrite(tempG, statModel, iterations):
    # Method to rewire the graph based on some probabaltic methods.
    # Does not increase or decrease the number of vertices or edges.
    # Will rewire the graph in place
    #https://graph-tool.skewed.de/static/doc/generation.html#graph_tool.generation.random_rewire

    print random_rewire(tempG, model = statModel, n_iter = iterations, edge_sweep = False)
    return tempG

if __name__ == "__main__":
    finalR = []
    row = ["GraphNumber", "GFPC-C", "GFPC-VC", "GFPC-GC", "NS"]
    finalR.append(row)
    resultFile = open('EXP1Results.txt', 'w')
    g = price_network(200000, m = 2, directed = False)
    g1 = Graph(g)
    rewireITR = [50000, 100000, 200000, 300000, 400000, 500000 ]
    graphNames = ["1.pdf", "2.pdf", "3.pdf", "4.pdf", "5.pdf", "6.pdf"]
    printDegreeDist(g1, "org.pdf")
    count = 0
    graphs = []

    for i in rewireITR:
        g2 = randomRewrite(g1, "erdos", i)
        graphs.append(g2)
        printDegreeDist(g2, graphNames[count])
        count = count + 1
        g1 = Graph(g)

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
