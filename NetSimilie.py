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
import os, csv
from tabulate import tabulate
import numpy
from scipy import stats
import scipy.spatial.distance

def netSmilieFeatureExtraction(tempG):
    print("Starting NS Feature Extraction")
    # 1) - number of neigbours of each vertex
    tempG.vertex_properties["dp"] = tempG.degree_property_map("total")

    # 2) - cluster coeffecient
    tempG.vertex_properties["lc"] = local_clustering(tempG)

    # 3) - Average number of nodes two hops away.....
    tempG.vertex_properties["tHN"] = tempG.new_vertex_property("double")

    # 4) - Average clustering coeffecient of the Neihbourhood of node i
    tempG.vertex_properties["nCCP"] = tempG.new_vertex_property("double")

    # 5) - Number of edges in i's egonet
    tempG.vertex_properties["nEEG"] = tempG.new_vertex_property("double")
    egoNet = tempG.new_vertex_property("bool")
    egoNet.a = False

    # 6) - Number of out going edges from the neigbourhood of node i
    tempG.vertex_properties["oEEG"] = tempG.new_vertex_property("double")

    # 7) - Number of neighbours of the egonet
    tempG.vertex_properties["oNEG"] = tempG.new_vertex_property("double")

    # iterate over the neighbour vertices of the current vertex starting from the first and going to the last
    for v in tempG.vertices():
        averageNeighbourhoodScore = 0
        twoHopAwayNeighbours = 0
        egoNet.a = False
        egoNet[v] = True

        for w in v.out_neighbours():
            # 3) - Average number of nodes two hops away
            # This is the out degree of the first neighbour (Assuming no parallel edges)
            twoHopAwayNeighbours += tempG.vp.dp[w]

            # 4) - Average clustering coeffecient of the Neihbourhood of node i
            averageNeighbourhoodScore += tempG.vp.lc[w]

            # 5) - Ego net
            egoNet[w] = True

        #------------------------NEIGHBOURHOOD FOR LOOP END------------------------#
        # Generate the EgoNet Graph
        egoNetGV = GraphView(tempG, vfilt=egoNet)
        egoOutEdges = 0
        numEgoNeigh = set()

        # 6) - Number of out going edges
        for egoV in egoNetGV.vertices():
            # Collect the number of out going edges from the Ego Net subtract by the number already in the egonet
            egoOutEdges += tempG.vp.dp[egoV]

            # Loop through each level 2 nodes and add to a set, then take the len to give the number of neghbours of the egonet
            for egoNetW in egoV.out_neighbours():
                numEgoNeigh.add(int(egoNetW))
        egoOutEdges = (egoOutEdges - egoNetGV.num_edges())

        # Store the computed results in the property maps of the graph
        if tempG.vp.dp[v] != 0:
            tempG.vp.tHN[v] = ((1.0 / float(tempG.vp.dp[v])) * float(twoHopAwayNeighbours))
            tempG.vp.nCCP[v] = ((1.0 / float(tempG.vp.dp[v])) * float(averageNeighbourhoodScore))
        else:
            tempG.vp.tHN[v] = ((1.0 / 1.0) * float(twoHopAwayNeighbours))
            tempG.vp.nCCP[v] = ((1.0 / 1.0) * float(averageNeighbourhoodScore))
        tempG.vp.nEEG[v] = egoNetGV.num_edges()
        tempG.vp.oEEG[v] = egoOutEdges
        tempG.vp.oNEG[v] = len(numEgoNeigh)

    #------------------------VERTEX FOR LOOP END------------------------#

    return tempG

def netSmilieFeatureAggregation(tempG):
    print("Starting NS Feature Aggregation")
    # Create node X feature matrix
    features = [ [], [], [], [], [], [], [] ]

    for v in tempG.vertices():
        features[0].append(tempG.vp.dp[v])
        features[1].append(tempG.vp.lc[v])
        features[2].append(tempG.vp.tHN[v])
        features[3].append(tempG.vp.nCCP[v])
        features[4].append(tempG.vp.nEEG[v])
        features[5].append(tempG.vp.oEEG[v])
        features[6].append(tempG.vp.oNEG[v])

    f = []
    for i in range(7):
        median = numpy.median(features[i])
        mean = numpy.mean(features[i])
        stdev = numpy.std(features[i])
        skewness = stats.skew(features[i])
        kurtosis = stats.kurtosis(features[i])
        f += [median, mean, stdev, skewness, kurtosis]

    return f

def netSimileCompare(f1, f2):
    print("Starting NS Feature Comparison")
    return abs(scipy.spatial.distance.canberra(f1, f2))


def netSimileSingleFingerprint(tempG):
    # Generate a FingerPrint for a single graph
    tempG = netSmilieFeatureExtraction(tempG)
    features = netSmilieFeatureAggregation(tempG)

    return features


def netSimileControl(G1, G2):
    tempG = netSmilieFeatureExtraction(G1)
    features = netSmilieFeatureAggregation(tempG)
    tempG2 = netSmilieFeatureExtraction(G2)
    features2 = netSmilieFeatureAggregation(tempG2)
    vertCompare = netSimileCompare(features, features2)

    return vertCompare

if __name__ == "__main__":

    g = price_network(20000, m = 2, directed = False)

    tempG = netSmilieFeatureExtraction(g)
    features = netSmilieFeatureAggregation(tempG)

    g2 = price_network(20000, m = 2, directed = False)
    tempG2 = netSmilieFeatureExtraction(g2)
    features2 = netSmilieFeatureAggregation(tempG2)

    print netSimileCompare(features, features2)
