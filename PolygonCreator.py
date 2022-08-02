#https://stackoverflow.com/questions/45831084/creating-a-polygon-in-python

import numpy as np
import random
import time
import datetime


def generateShape(count):

    # ordered coordinates
    points = {}

    # 0 = CW; 1 = CCW
    orientation = random.randint(0,1)

    # 3-100 vertices
    numVertex = random.randint(0,17) + 3

    # randomly generates vertices
    xPoints = np.random.randint(0, 150, numVertex)
    yPoints = np.random.randint(0, 150, numVertex)

    # calculates center
    center = (np.average(xPoints), np.average(yPoints))

    # gets angles of vertices in relation to its distance from center and a line downwards (from center) with arctan2
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

    file = open(("polygons/polygon%s.txt" % count), "w")

    # labels vertices in relation to the randomly-generated CW/CCW orientation
    for i, coordinate in enumerate(coordinates):

        # CW
        if (orientation == 0):
            #plt.annotate(str(i + 1), coordinate)
            points[i] = coordinate

        # CCW
        else:
            if (i == 0):
                #plt.annotate(str(i + 1), coordinate)
                points[i] = coordinate
            else:
                #plt.annotate(str((numVertex + 1) - i), coordinate)
                points[numVertex - i] = coordinate

    # sorts polygon vertices by their index
    points = sorted(points.items(), key=lambda z: z[0])

    if (orientation == 0):
        file.write("CW\n")
    else:
        file.write("CCW\n")

    # writes to file
    for index, coords in points:
        file.write("%s %s %s\n" % (index, coords[0], coords[1]))

    file.close()

if __name__ == "__main__":
    for i in range(1, 25):
        generateShape(i)
