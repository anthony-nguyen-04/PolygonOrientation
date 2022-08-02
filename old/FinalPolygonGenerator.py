#https://stackoverflow.com/questions/45831084/creating-a-polygon-in-python

import numpy as np
from matplotlib import pyplot as plt
import time
import datetime

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

def generateShape(x):

    # ordered coordinates
    points = {}

    # 0 = CW; 1 = CCW
    # I know that randint is inclusive, but i cannot roll a 1 to save my life with randint(1)
    orientation = np.random.randint(2)

    # 3-100 vertices
    numVertex = np.random.randint(97) + 3

    # randomyl generates vertices
    xPoints = np.random.randint(0, 150, numVertex)
    yPoints = np.random.randint(0, 150, numVertex)

    center = (np.average(xPoints), np.average(yPoints))

    # gets angles of vertices in relation to its distance from center and (0,-1) with arctan2
    # sorts by angle to get edges in-order
    angles = np.arctan2(xPoints - center[0], yPoints - center[1])
    sortedPoints = sorted([(x, y, angle) for x, y, angle in zip(xPoints, yPoints, angles)], key = lambda z : z[2])

    # set(sortedPoints) removes duplicates because set properties
    # if lengths are different, duplicates existed
    if len(sortedPoints) != len(set(sortedPoints)):
        raise Exception('two equal coordinates -- exiting')

    # takes (x,y,angle) to (x), (y), (angles [unused])
    xSorted, ySorted, _ = zip(*sortedPoints)
    xSorted = list(xSorted)
    ySorted = list(ySorted)

    # gets coordinates
    coordinates = zip(xSorted.copy(), ySorted.copy())

    # appends first point to end to have loop
    xSorted.append(xSorted[0])
    ySorted.append(ySorted[0])

    # labels vertices in relation to the randomly-generated CW/CCW orientation
    for i, coordinate in enumerate(coordinates):
        # CW
        if (orientation == 0):
            #plt.annotate(str(i + 1), coordinate)
            points[i] = coordinate

        # CCW
        else:
            if (i+1 == 1):
                #plt.annotate(str(i + 1), coordinate)
                points[i] = coordinate
            else:
                #plt.annotate(str((numVertex + 1) - i), coordinate)
                points[numVertex - i] = coordinate


    # sorts points by y-value
    ascendingPoints = sorted(points.items(), key = lambda z: z[1][1])

    # from lowest y-value vertices, find the one with highest x-value
    # ensures that at least one of its adjacent vertices does not have same y-value
    bottomLevelPoints = [z for z in ascendingPoints if z[1][1] == (ascendingPoints[0])[1][1]]
    bottomLevelPoints = sorted(bottomLevelPoints, key = lambda  z: z[1][0])
    bottomPoint = bottomLevelPoints[-1]
    bottomIndex = bottomPoint[0]

    # uses a separate algorithm (based off of cross product of vectors from bottom-most point)
    # solves for orientation of polygon

    # used to get vectors originating from "bottom" vertex
    (xCenter, yCenter) = points[bottomIndex]
    (xBefore, yBefore) = points[(bottomIndex - 1) % numVertex]
    (xAfter, yAfter) = points[(bottomIndex + 1) % numVertex]

    vectorBefore = (xBefore - xCenter, yBefore - yCenter)
    vectorAfter = (xAfter - xCenter, yAfter - yCenter)

    vectorBefore = np.asarray(vectorBefore)
    vectorAfter = np.asarray(vectorAfter)

    # cross product
    cross = np.cross(vectorBefore, vectorAfter)

    # from the cross product, solves for orientation without help from given orientation
    calculatedOrientation = checkDirection(cross)

    # saves figure every 1000 iteraitons
    if (x % 1000 == 0):

        # plots and annotate points
        plt.plot(xSorted, ySorted)
        for i in points.keys():
            plt.annotate(i, points[i])

        # the orientation used to create the polygon
        if orientation == 0 :
            realOr = "CW"
        elif orientation == 1:
            realOr = "CCW"
        else:
            realOr = "ERROR"

        # the predicted orientation for the polygon
        if calculatedOrientation == 0 :
            predOr = "CW"
        elif calculatedOrientation == 1:
            predOr = "CCW"
        else:
            predOr = "ERROR"

        # saves figure, before closing
        plt.savefig(str("%s|%s + %s.png" % (realOr, predOr, x)))

        plt.clf()
        plt.close()

    # returns True/False to see if prediction is correct or not

    if (orientation == calculatedOrientation):
        return True
    else:

        print("---")
        print("Iteration %s" % x)
        print("%s versus %s" % (orientation, calculatedOrientation))

        # if not equal, print data logs
        print(ascendingPoints)
        print(bottomLevelPoints)
        print(bottomPoint)
        print(bottomIndex)
        print(vectorBefore)
        print(vectorAfter)
        print(cross)
        print("---")

        return False

def main():

    # timer
    startTime = time.perf_counter()

    success = 0
    failure = 0
    duplicate = 0

    iterations = 10000

    # runs iterations
    for x in range(iterations):
        if (x % (int(iterations / 5)) == 0):
            print("CLOSER")

        try:
            result = generateShape(x)
            if result:
                success = success + 1
            else:
                failure = failure + 1

        except:
            duplicate = duplicate + 1

    print("PASS %s // FAIL %s // DUPE %s" % (success, failure, duplicate))

    print(str(datetime.timedelta(seconds = time.perf_counter() - startTime)))



if __name__ == "__main__":
    main()
    #generateShape(0)
