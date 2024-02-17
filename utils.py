import math

def distance(x1,y1,x2,y2):
    return math.hypot(x2 - x1, y2 - y1)

def readfile(name):
    with open(name,"rb") as f:
        return f.read().decode("utf-8")
