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

def checkPolygon(polygonText):
    points = {}

    # opens specified txt file with polygon coordinates
    file = open("polygons/%s" % polygonText)

    # skips the orientation
    file.readline()

    # checks if file still has content
    while(len(line := file.readline()) != 0):

        # parses x,y coordinates for polygon vertices
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
    x, y = points[bottomIndex]
    xBefore, yBefore = points[(bottomIndex - 1) % len(points)]
    xAfter, yAfter = points[(bottomIndex + 1) % len(points)]

    # calculates vectors from vertex
    vectorBefore = (xBefore - x, yBefore - y)
    vectorAfter = (xAfter - x, yAfter - y)

    vectorBefore = np.asarray(vectorBefore)
    vectorAfter = np.asarray(vectorAfter)

    # cross product of vectors originating from bottom-most vertex
    cross = np.cross(vectorBefore, vectorAfter)

    # from the cross product, solves for orientation
    calculatedOrientation = checkDirection(cross)

    if calculatedOrientation == 0:
        #print("%s : CW" % i)
        return("CW")
    elif calculatedOrientation == 1:
        #print("%s : CCW" % i)
        return("CCW")
    else:
        raise Exception('collinear points -- exiting')

def checkAllVertices(polygonText):

    # voting system to see if polygon is CW or CCW
    vote = {"CW" : 0, "CCW" : 0}

    points = {}

    # opens specified txt file with polygon coordinates
    file = open("polygons/%s" % polygonText)

    # checks if file still has content
    while (len(line := file.readline()) != 0):
        # parses x,y coordinates for polygon vertices
        parts = [int(x) for x in line.split()]

        points[parts[0]] = (parts[1], parts[2])

    # iterates over all vertices of polygon
    for index in range(len(points)):

        # used to get vectors originating from vertex
        x,y = points[index]
        xBefore, yBefore = points[(index - 1) % len(points)]
        xAfter, yAfter = points[(index + 1) % len(points)]

        # calculates vectors from vertex
        vectorBefore = (xBefore - x, yBefore - y)
        vectorAfter = (xAfter - x, yAfter - y)

        vectorBefore = np.asarray(vectorBefore)
        vectorAfter = np.asarray(vectorAfter)

        # cross product of vectors originating from particular vertex
        cross = np.cross(vectorBefore, vectorAfter)

        # from the cross product, solves for orientation as seen from particular vertex
        calculatedOrientation = checkDirection(cross)

        # based on orientation calculated from vertex perspective,
        # puts vote for overall polygon orientation
        if calculatedOrientation == 0:
            vote["CW"] = vote["CW"] + 1
        elif calculatedOrientation == 1:
            vote["CCW"] = vote["CCW"] + 1
        else:
            raise Exception('collinear points -- exiting')

    return(vote)

def checkPolygonOrientationEqual(polygonText):
    points = {}

    # opens specified txt file with polygon coordinates
    file = open("polygons/%s" % polygonText)

    # stores given orientation
    if ((fileOrientation := file.readline()).__eq__("CW\n")):
        orientation = 0
    elif (fileOrientation.__eq__("CCW\n")):
        orientation = 1
    else:
        raise Exception("Unknown given orientation")

    # checks if file still has content
    while(len(line := file.readline()) != 0):

        # parses x,y coordinates for polygon vertices
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
    x, y = points[bottomIndex]
    xBefore, yBefore = points[(bottomIndex - 1) % len(points)]
    xAfter, yAfter = points[(bottomIndex + 1) % len(points)]

    # calculates vectors from vertex
    vectorBefore = (xBefore - x, yBefore - y)
    vectorAfter = (xAfter - x, yAfter - y)

    vectorBefore = np.asarray(vectorBefore)
    vectorAfter = np.asarray(vectorAfter)

    # cross product of vectors originating from bottom-most vertex
    cross = np.cross(vectorBefore, vectorAfter)

    # from the cross product, solves for orientation
    calculatedOrientation = checkDirection(cross)

    if calculatedOrientation == orientation:
        return True
    else:
        return False

def graphPolygon(polygonText):
    points = {}

    # opens specified txt file with polygon coordinates
    file = open("polygons/%s" % polygonText)

    # checks if file still has content
    while (len(line := file.readline()) != 0):
        # parses x,y coordinates for polygon vertices
        parts = [int(x) for x in line.split()]

        points[parts[0]] = (parts[1], parts[2])

    # makes separate lists for x and y coordinates for polygon vertices
    xSorted = list(map(lambda x: x[0], points.values()))
    ySorted = list(map(lambda x: x[1], points.values()))

    # appends the first point to the end, in order to make polygon connected
    xSorted.append(points[0][0])
    ySorted.append(points[0][1])

    # plot and annotate points
    plt.plot(xSorted, ySorted)

    for j in points.keys():
        plt.annotate(j, points[j])

    # saves plot to file
    plt.savefig("%s.png" % (polygonText.split("."))[0])

    # shows polygon
    # plt.show()

    # closes plot
    plt.clf()
    plt.close()

def checkRandom(amount):
    # parses total amount of polygon files
    numPolygons = len(glob.glob("polygons/*.txt"))

    # generates sample group of polygons to run tests on
    for i in random.sample(range(1, numPolygons + 1), k=amount):
        print("%s : %s, %s" % (i, checkPolygonOrientationEqual("polygon%s.txt" % i), checkPolygon("polygon%s.txt" % i)))

if __name__ == "__main__":
    checkRandom(10)