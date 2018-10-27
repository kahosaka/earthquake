'''
World Wide Earthquake Watch
Author: Kiana Hosaka
Credits: Chapter 7 of Miller and Ranum text.
Description: Uses file processing and data mining to discover patterns of earthquake activity
around world over past year. Plots the results onto a world map.
'''

import math
import random
import turtle
import doctest


def readFile(filename):
    """
    (str) -> dict
    Opens the file then creates and returns dict of the latitude and longitude.
    >>> readFile("test.txt") #small file
    {1: [142.8358, -6.2147], 2: [150.7321, -60.1778], 3: [142.8469, -6.0855], 4: [142.9858, -6.3589], 5: [143.203, -6.3793], 6: [142.7909, -6.3225], 7: [143.0483, -6.4178], 8: [169.2939, -18.8524]}
    """
    with open(filename, "r") as datafile:
        line = datafile.readline()
        datadict = {}
        key = 0

        for aline in datafile:
            items = aline.strip().split(",")
            key = key + 1
            lat = float(items[1])
            lon = float(items[2])
            datadict[key] = [lon, lat]

    return datadict

def euclidD(point1, point2):
    """
    (tuple, tuple) -> float
    Computes and returns the Euclidean distance between two points.
    >>> euclidD((2,6),(3,10)) #small numbers
    4.123105625617661
    >>> euclidD((-35, 76), (-56,-26)) #negative numbers, large numbers
    104.1393297462587
    """
    total = 0
    for index in range(len(point1)):
        diff = (point1[index] - point2[index]) ** 2 #difference is index of point1 minus distance of point2 to 2 power
        total = total + diff #total is equal to the total plus difference

    euclidDistance = math.sqrt(total) #euclidean distance is the square root of the total
    return euclidDistance

def createCentroids(k, datadict):
    """
    (int, dict) -> list
    Chooses k random centroids. Can't use doctest because of random
    produces different outputs. Returns the list of centroids.
    """
    centroids = []
    centroidCount = 0
    centroidKey = []

    while centroidCount < k:
        rkey = random.randint(1, len(datadict)) #rkey is the random key chosen from 1 to the length of datadict

        if rkey not in centroidKey:
            centroids.append(datadict[rkey]) #append to centroids
            centroidKey.append(rkey) #append to centroidKey
            centroidCount = centroidCount + 1

    return centroids

def createClusters(k, centroids, datadict, repeats):
    """
    (int, list, dict, int) -> list
    Takes the number of clusters (k), centroids, data dictionary,
    and the number of repetitions. Creates and returns the list of clusters.
    >>> createClusters(6,[[149.6847, 45.0761], [102.1165, -4.1281], [-66.9686, -24.146], [161.3147, -10.4057], [-27.479, -56.0782], [128.5781, 2.3103]],   {1: [-90.9718, 13.7174], 2: [-66.9686, -24.146], 3: [149.6847, 45.0761], 4: [161.3147, -10.4057], 5: [179.4232, 52.1764], 6: [102.1165, -4.1281], 7: [128.5781, 2.3103], 8: [132.036, 32.8717], 9: [-27.479, -56.0782]}, 7)
    ****PASS 0 ****
    ****PASS 1 ****
    ****PASS 2 ****
    ****PASS 3 ****
    ****PASS 4 ****
    ****PASS 5 ****
    ****PASS 6 ****
    [[3, 5, 8], [6], [1, 2], [4], [9], [7]]
    """
    #FOR APASS
    for apass in range(repeats):
        print("****PASS", apass, "****")
        clusters = [] #empty list of clusters
        for i in range(k):
            clusters.append([]) #append

        #FOR AKEY
        for akey in datadict:
            distances = [] #empty list of distances
            for clusterIndex in range(k):
                dist = euclidD(datadict[akey], centroids[clusterIndex])
                distances.append(dist) #append dist to distances list

            mindist = min(distances) #minimum distance
            index = distances.index(mindist)

            clusters[index].append(akey) #append this

        dimensions = len(datadict[1])

        #FOR CLUSTERINDEX
        for clusterIndex in range(k):
            sums = [0]*dimensions
            for akey in clusters[clusterIndex]:
                datapoints = datadict[akey]
                for ind in range(len(datapoints)):
                    sums[ind] = sums[ind] + datapoints[ind]
            for ind in range(len(sums)):
                clusterLen = len(clusters[clusterIndex])
                if clusterLen != 0: #if not equal to 0
                    sums[ind] = sums[ind]/clusterLen

            centroids[clusterIndex] = sums

    return clusters

def visualizeQuakes(dataFile):
    """
    (str) -> None
    Visualizes the earthquake clusters. Calls other readFile,
    createCentroids, createClusters, and visualizeQuakes. Returns None.
    > visualizeQuakes("tester.txt") will print:
    ****PASS 0 ****
    ****PASS 1 ****
    ****PASS 2 ****
    ****PASS 3 ****
    ****PASS 4 ****
    ****PASS 5 ****
    ****PASS 6 ****
    and the map will pop up
    """
    datadict = readFile(dataFile)
    quakeCentroids = createCentroids(6, datadict)
    clusters = createClusters(6, quakeCentroids, datadict, 7)

    draw = eqDraw(6, datadict, clusters)

    return None

def eqDraw(k, eqDict, eqClusters):
    """
    (int, dict, list) -> None
    Called by visualizeQuakes to do work of plotting results of k-means
    analysis on the world map. Returns None.
    # EXAMPLES OF USE: This function is called by visualizeQuakes to plot points on the map.
    """
    quakeT = turtle.Turtle()
    quakeWin = turtle.Screen()
    quakeWin.bgpic("worldmap1800_900.gif")
    quakeWin.screensize(1800, 900)

    wFactor = (quakeWin.screensize()[0]/2)/180
    hFactor = (quakeWin.screensize()[1]/2)/90

    quakeT.hideturtle()
    quakeT.up()

    colorlist = ["red", "green", "blue", "orange", "cyan", "yellow"]

    for clusterIndex in range(k):
        quakeT.color(colorlist[clusterIndex])
        for akey in eqClusters[clusterIndex]:
            lon = eqDict[akey][0]
            lat = eqDict[akey][1]
            quakeT.speed("fastest")
            quakeT.goto(lon*wFactor, lat*hFactor)
            quakeT.dot()
    quakeWin.exitonclick()

    return None


def main():
    """
    () -> None
    Top level function that assigns values to k, r, f, and
    calls visualizeQuakes. Returns None.
    """
    print(doctest.testmod())
    k = 6
    r = 7
    f = "earthquakes.txt"

    createClusters(k, createCentroids(k,readFile(f)), readFile(f), r)
    visualizeQuakes(f)

    return None

main()
