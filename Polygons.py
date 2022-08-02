from PolygonCreator import generateShape
from PolygonChecker import checkRandom
from PolygonChecker import checkPolygonOrientationEqual

if __name__ == "__main__":
    for i in range(1, 25):
        generateShape(i)
    checkRandom(10)