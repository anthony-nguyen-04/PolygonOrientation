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

    #print(numVertex)
    #print(orientation)

    xPoints = np.random.randint(0, 150, numVertex)
    yPoints = np.random.randint(0, 150, numVertex)

    center = (np.average(xPoints), np.average(yPoints))

    # gets angles of vertices in relation to (0,-1) with arctan2
    # sorts by angle to get edges in-order
    angles = np.arctan2(xPoints - center[0], yPoints - center[1])
    sortedPoints = sorted([(x, y, angle) for x, y, angle in zip(xPoints, yPoints, angles)], key = lambda z : z[2])

    # set(sortedPoints) removes duplicates because set properties
    # if lengths are different, duplicates existed
    if len(sortedPoints) != len(set(sortedPoints)):
        raise Exception('two equal coordinates -- exiting')


    # takes (x,y,angle) to (x), (y), (angles) [unused]
    xSorted, ySorted, _ = zip(*sortedPoints)
    xSorted = list(xSorted)
    ySorted = list(ySorted)

    # gets coordinates
    coordinates = zip(xSorted.copy(), ySorted.copy())

    # appends first point to end to have loop
    xSorted.append(xSorted[0])
    ySorted.append(ySorted[0])

    # labels vertices
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


    ascendingPoints = sorted(points.items(), key = lambda z: z[1][1])
    bottomLevelPoints = [z for z in ascendingPoints if z[1][1] == (ascendingPoints[0])[1][1]]
    bottomLevelPoints = sorted(bottomLevelPoints, key = lambda  z: z[1][0])

    bottomPoint = bottomLevelPoints[-1]
    bottomIndex = bottomPoint[0]

    (xCenter, yCenter) = points[bottomIndex]
    (xBefore, yBefore) = points[(bottomIndex - 1) % numVertex]
    (xAfter, yAfter) = points[(bottomIndex + 1) % numVertex]

    vectorBefore = (xBefore - xCenter, yBefore - yCenter)
    vectorAfter = (xAfter - xCenter, yAfter - yCenter)

    vectorBefore = np.asarray(vectorBefore)
    vectorAfter = np.asarray(vectorAfter)

    cross = np.cross(vectorBefore, vectorAfter)

    calculatedOrientation = checkDirection(cross)


    if (x % 1000 == 0):

        plt.plot(xSorted, ySorted)
        for i in points.keys():
            plt.annotate(i, points[i])

        if orientation == 0 :
            orName = "CW"
        elif orientation == 1:
            orName = "CCW"
        else:
            orName = "DUPE"

        plt.savefig(str("%s + %s.png" % (orName, x)))

        plt.clf()
        plt.close()


    #if (orientation == 0):
    #    print("IS CLOCKWISE")
    #else:
    #    print("IS COUNTERCLOCKWISE")


    #if (calculatedOrientation == 0):
    #    print("IS CALCULATED CLOCKWISE")
    #else:
    #    print("IS CALCULATED COUNTERCLOCKWISE")

    #plt.plot(xSorted, ySorted)
    #plt.savefig(str("wrong%s + %s + %s.png" % (x, orientation, calculatedOrientation)))
    #plt.show()


    if (orientation == calculatedOrientation):
        #print("TRUE")
        return True
    else:
        #print("FALSE")

        print("---")
        print("Iteration %s" % x)
        print("%s versus %s" % (orientation, calculatedOrientation))

        # printing data logs
        print(ascendingPoints)
        print(bottomLevelPoints)
        print(bottomPoint)
        print(bottomIndex)
        print(vectorBefore)
        print(vectorAfter)
        print(cross)
        print("---")

        #plt.plot(xSorted, ySorted)
        #plt.savefig(str("wrong%s.png" % x))
        #plt.show()
        #plt.close()
        return False



    #print(checkDirection(cross))

    #plt.show()

    #print(center)
    #print(sortedPoints)
    #print(xSorted)
    #print(ySorted)
    #print(*coordinates)

def main():

    startTime = time.perf_counter()

    success = 0
    failure = 0
    duplicate = 0

    iterations = 10000

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