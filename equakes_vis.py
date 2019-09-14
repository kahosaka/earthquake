'''
Earthquake Visualizer 2017
Author: Kiana Hosaka
Credits: Chapter 7 of Miller and Ranum text.
Description: Discovered patterns of earthquake activity around the world over
the past year using file processing and data mining. Plots the results onto
a world map.
'''

import math
import random
import turtle
import doctest

def readFile(filename):
    """
    (str) -> dict
    Opens the file then creates and returns dict of the latitude and longitude.
    >>> readFile("test.txt") # Small file
    {1: [142.8358, -6.2147], 2: [150.7321, -60.1778], 3: [142.8469, -6.0855], 4: [142.9858, -6.3589], 5: [143.203, -6.3793], 6: [142.7909, -6.3225], 7: [143.0483, -6.4178], 8: [169.2939, -18.8524]}
    """
    with open(filename, "r") as data_file:
        line = data_file.readline()
        data_dict = {}
        key = 0

        for a_line in data_file:
            items = a_line.strip().split(",")
            key = key + 1
            lat = float(items[1])
            lon = float(items[2])
            data_dict[key] = [lon, lat]

    return data_dict

def euclidD(point1, point2):
    """
    (tuple, tuple) -> float
    Computes and returns the Euclidean distance between two points.
    >>> euclidD((2,6),(3,10)) # Small numbers
    4.123105625617661
    >>> euclidD((-35, 76), (-56,-26)) # Negative and large numbers
    104.1393297462587
    """
    total = 0
    for index in range(len(point1)):
        diff = (point1[index] - point2[index]) ** 2 # Difference is index of point1 minus distance of point2 to 2 power
        # total = total + diff # Add difference to total
        total += diff # Add difference to total

    euclid_dist = math.sqrt(total) # Euclidean distance is the square root of the total

    return euclid_dist

def createCentroids(k, data_dict):
    """
    (int, dict) -> list
    Chooses k random centroids. Returns the list of centroids.
    (Not using doctest because inconsistent outputs are expected.)
    """
    centroids = []
    centroid_cnt = 0
    centroid_key = []

    while centroid_cnt < k:
        rand_key = random.randint(1, len(data_dict)) # rkey is the random key chosen from 1 to the length of data_dict

        if rand_key not in centroid_key:
            centroids.append(data_dict[rand_key]) # Append to centroids
            centroid_key.append(rand_key) # Append to centroid_key
            centroid_cnt = centroid_cnt + 1

    return centroids

def createClusters(k, centroids, data_dict, repeats):
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
    # For each pass in number of repeats...
    for a_pass in range(repeats):
        print("****PASS", a_pass, "****")
        clusters = []
        # Append an empty list for each cluster
        for i in range(k):
            clusters.append([])
        # For each key...
        for key in data_dict:
            distances = []
            for cluster_index in range(k):
                # Calculate the euclidean distance between coordinates and centroids
                dist = euclidD(data_dict[key], centroids[cluster_index])
                distances.append(dist)

            min_dist = min(distances)
            index = distances.index(min_dist) # Index of the minimum distance
            clusters[index].append(key) # Append key of minimum distance cluster

        dimensions = len(data_dict[1])

        # For each cluster...
        for cluster_index in range(k):
            sums = [0] * dimensions
            for key in clusters[cluster_index]:
                data_points = data_dict[key]
                for ind in range(len(data_points)):
                    sums[ind] = sums[ind] + data_points[ind]
            for ind in range(len(sums)):
                cluster_len = len(clusters[cluster_index])
                if cluster_len != 0: # If not equal to 0
                    sums[ind] = sums[ind]/cluster_len

            centroids[cluster_index] = sums

    return clusters

def visualizeQuakes(data_file):
    """
    (str) -> None
    Visualizes the earthquake clusters. Calls other readFile,
    createCentroids, createClusters, and visualizeQuakes. Returns None.
    """
    data_dict = readFile(data_file)
    quake_centroids = createCentroids(6, data_dict)
    clusters = createClusters(6, quake_centroids, data_dict, 7)

    draw = eqDraw(6, data_dict, clusters)

    return None

def eqDraw(k, eq_dict, eq_clusters):
    """
    (int, dict, list) -> None
    Called by visualizeQuakes to do work of plotting results of k-means
    analysis on the world map. Returns None.
    # EXAMPLES OF USE: This function is called by visualizeQuakes to plot points on the map.
    """
    quake_t = turtle.Turtle()
    quake_window = turtle.Screen()
    quake_window.bgpic("worldmap1800_900.gif")
    quake_window.screensize(1800, 900)

    width = (quake_window.screensize()[0]/2)/180
    height = (quake_window.screensize()[1]/2)/90

    quake_t.hideturtle()
    quake_t.up()

    color_list = ["red", "green", "blue", "orange", "cyan", "yellow"]

    for cluster_index in range(k):
        quake_t.color(color_list[cluster_index])
        for key in eq_clusters[cluster_index]:
            lon = eq_dict[key][0]
            lat = eq_dict[key][1]
            quake_t.speed("fastest")
            quake_t.goto(lon*width, lat*height)
            quake_t.dot()
    quake_window.exitonclick()

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
