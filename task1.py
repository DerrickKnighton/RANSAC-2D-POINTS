"""
RANSAC Algorithm Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to fit a line to the given points using RANSAC algorithm, and output
the names of inlier points and outlier points for the line.

Do NOT modify the code provided to you.
Do NOT use ANY API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import ANY library (function, module, etc.).
You can use the library random
Hint: It is recommended to record the two initial points each time, such that you will Not 
start from this two points in next iteration.
"""
import random



def calculateInliers(input_points,point1,point2,highIntercept,lowintercept,slope):
    #print(point1,point2,slope)
    inlier_points_name = []
    inlier_points_name.append(point1['name'])
    inlier_points_name.append(point2['name'])
    outlier_points_name = []
    for x in input_points:
        if point1['name'] != x['name'] and point2['name'] != x['name']:
            #calculate x and y for highintercept and lowintercept
            yhigh = (slope * x['value'][0]) + highIntercept
            ylow = (slope * x['value'][0]) + lowintercept
            xhigh = (x['value'][1] - highIntercept) / slope
            xlow = (x['value'][1] - lowintercept) / slope
            if yhigh >= x['value'][1] and ylow <= x['value'][1]:
                if slope > 0 and xhigh <= x['value'][0] and xlow >= x['value'][0]:
                    inlier_points_name.append(x['name'])
                elif slope < 0 and xhigh >= x['value'][0] and xlow <= x['value'][0]:
                    inlier_points_name.append(x['name'])
                elif slope > 0 and xhigh >= x['value'][0] and xlow <= x['value'][0]:
                    outlier_points_name.append(x['name'])
                elif slope < 0 and xhigh <= x['value'][0] and xlow >= x['value'][0]:
                    outlier_points_name.append(x['name']) 
            else:
                outlier_points_name.append(x['name'])
    return inlier_points_name,outlier_points_name
                        
                        
                        
def findIntercept(slope,point1,t):
    #print(slope,point1)
    intercept = point1[1] - (slope * point1[0])
    #print(intercept,point1)
    return intercept + t, intercept - t

def calculateInlinersHS(input_points,point1,point2,t):
    higherY = point1['value'][1] + t
    lowerY = higherY - 2*t
    #print(higherX,lowerX)
    inlier_points_name = []
    inlier_points_name.append(point1['name'])
    inlier_points_name.append(point2['name'])
    outlier_points_name = []
    for x in input_points:
        if point1['name'] != x['name'] and point2['name'] != x['name']:
            if x['value'][1] <= higherY and x['value'][1] >= lowerY:
                inlier_points_name.append(x['name'])
            else:
                outlier_points_name.append(x['name'])
    return inlier_points_name,outlier_points_name



def calculateInlinersVS(input_points,point1,point2,t):
    higherX = point1['value'][0] + t
    lowerX = higherX - 2*t
    #print(higherX,lowerX)
    inlier_points_name = []
    inlier_points_name.append(point1['name'])
    inlier_points_name.append(point2['name'])
    outlier_points_name = []
    for x in input_points:
        if point1['name'] != x['name'] and point2['name'] != x['name']:
            if x['value'][0] <= higherX and x['value'][0] >= lowerX:
                inlier_points_name.append(x['name'])
            else:
                outlier_points_name.append(x['name'])
    return inlier_points_name,outlier_points_name

def computeSlope(point1,point2):
    #print(point1,point2)
    try:
        return((point2[1]-point1[1])/(point2[0]-point1[0]))
    except ZeroDivisionError:
       # print("vertical slope")
        return -1000

def solution(input_points, t, d, k):
    """
    :param input_points:
           t: t is the perpendicular distance threshold from a point to a line
           d: d is the number of nearby points required to assert a model fits well, you may not need this parameter
           k: k is the number of iteration times
           Note that, n for line should be 2
           (more information can be found on the page 90 of slides "Image Features and Matching")
    :return: inlier_points_name, outlier_points_name
    inlier_points_name and outlier_points_name is two list, each element of them is str type.
    For example: If 'a','b' is inlier_points and 'c' is outlier_point.
    the output should be two lists of ['a', 'b'], ['c'].
    Note that, these two lists should be non-empty.
    """
    numOfPoints = len(input_points)
    #will update k with pair of points checked 
    inlier_points_name = []
    outlier_points_name = []
    x = 0
    while x < numOfPoints:
        if input_points[x]['name'] != 'h':
            y = x+1
            while y < numOfPoints:
                #print(input_points[x]['name'],input_points[y]['name'])
                slope = computeSlope(input_points[x]['value'],input_points[y]['value'])
                if slope == -1000:
                    #vertical slope
                    tempIn,tempout = calculateInlinersVS(input_points,input_points[x],input_points[y],t)
                    if len(tempIn) > len(inlier_points_name):
                        inlier_points_name = tempIn
                        outlier_points_name = tempout
                elif slope == 0:
                    #horizontal slope
                    #print(input_points[x]['value'],input_points[y]['value'])
                    tempIn,tempout = calculateInlinersHS(input_points,input_points[x],input_points[y],t)
                    if len(tempIn) > len(inlier_points_name):
                        inlier_points_name = tempIn
                        outlier_points_name = tempout
                else:
                    #non vertical/horizontal slope more complicated
                    #finds intercept needed to calc inliners
                    highIntercept,lowintercept = findIntercept(slope,input_points[x]['value'],t)
                    tempIn,tempout = calculateInliers(input_points,input_points[x],input_points[y],highIntercept,lowintercept,slope)
                    if len(tempIn) > len(inlier_points_name):
                        inlier_points_name = tempIn
                        outlier_points_name = tempout
                    #print(slope)
                y+=1
        x+=1
      
        
    return inlier_points_name,outlier_points_name


if __name__ == "__main__":
    input_points = [{'name': 'a', 'value': (0.0, 1.0)}, {'name': 'b', 'value': (2.0, 1.0)},
                    {'name': 'c', 'value': (3.0, 1.0)}, {'name': 'd', 'value': (0.0, 3.0)},
                    {'name': 'e', 'value': (1.0, 2.0)}, {'name': 'f', 'value': (1.5, 1.5)},
                    {'name': 'g', 'value': (1.0, 1.0)}, {'name': 'h', 'value': (1.5, 2.0)}]
    t = 0.5
    d = 3
    k = 100
    inlier_points_name, outlier_points_name = solution(input_points, t, d, k)  # TODO
    print(len(inlier_points_name))
    print(len(outlier_points_name))
    for x in inlier_points_name:
        print(x)
    for y in outlier_points_name:
        print(y)
    assert len(inlier_points_name) + len(outlier_points_name) == 8  
    f = open('./results/task1_result.txt', 'w')
    f.write('inlier points: ')
    for inliers in inlier_points_name:
        f.write(inliers + ',')
    f.write('\n')
    f.write('outlier points: ')
    for outliers in outlier_points_name:
        f.write(outliers + ',')
    f.close()


