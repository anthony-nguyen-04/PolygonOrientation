import glob
import random
from matplotlib import pyplot as plt
import numpy as np

def checkDirection(zCross):
    if zCross > 0:
        return 0
        # "CLOCKWISE"
    elif zCross < 0:
        return 1
        # "COUNTER-CLOCKWISE"
    else:
        print("COLLINEAR")
        return -1
        # "N/A"

def checkPolygons(amount):
    numPolygons = len(glob.glob("polygons/*.txt"))
    for i in random.sample(range(1, numPolygons + 1), k=amount):
        points = {}

        file = open("polygons/polygon%s.txt" % i)
        while(len(line := file.readline()) != 0):
            parts = [int(x) for x in line.split()]

            points[parts[0]] = (parts[1], parts[2])

        # sorts points by y-value
        ascendingPoints = sorted(points.items(), key=lambda z: z[1][1])

        # from lowest y-value vertices, find the one with highest x-value
        # ensures that at least one of its adjacent vertices does not have same y-value
        bottomLevelPoints = [z for z in ascendingPoints if z[1][1] == (ascendingPoints[0])[1][1]]
        bottomLevelPoints = sorted(bottomLevelPoints, key=lambda z: z[1][0])
        bottomPoint = bottomLevelPoints[-1]
        bottomIndex = bottomPoint[0]

        # uses a separate algorithm (based off of cross product of vectors from bottom-most point)
        # solves for orientation of polygon

        # used to get vectors originating from "bottom" vertex
        (xCenter, yCenter) = points[bottomIndex]
        (xBefore, yBefore) = points[(bottomIndex - 1) % len(points)]
        (xAfter, yAfter) = points[(bottomIndex + 1) % len(points)]

        vectorBefore = (xBefore - xCenter, yBefore - yCenter)
        vectorAfter = (xAfter - xCenter, yAfter - yCenter)

        vectorBefore = np.asarray(vectorBefore)
        vectorAfter = np.asarray(vectorAfter)

        # cross product
        cross = np.cross(vectorBefore, vectorAfter)

        # from the cross product, solves for orientation without help from given orientation
        calculatedOrientation = checkDirection(cross)

        print("%s : %s" % (i, calculatedOrientation))

        # makes sorted list of x and y coordinates
        xSorted = list(map(lambda x: x[0], points.values()))
        ySorted = list(map(lambda x: x[1], points.values()))

        # appends the first point to the end, in order to make polygon connected
        xSorted.append(points[0][0])
        ySorted.append(points[0][1])

        # plots and annotate points
        plt.plot(xSorted, ySorted)

        for j in points.keys():
            plt.annotate(j, points[j])

        # saves plot to file
        plt.savefig(str("polygon%s orientation %s.png" % (i, calculatedOrientation)))

        plt.clf()
        plt.close()

if __name__ == "__main__":
    checkPolygons(5)
