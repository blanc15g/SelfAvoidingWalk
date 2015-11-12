# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:51:28 2015

@author: guy
"""

#IMPORTS
from __future__ import print_function, division
import random
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import linregress
 

    
    
#CONSTANT
numIterations = 5000             #More iterations for more accuracy but takes more time.    

#STORAGE ARRAYS    
distanceNaive = []                  #will store distances for each path length less than 1500
for i in range(1500):               #this is for the naive algorithm
    distanceNaive.append([])        #list of distances for each path length
    
distanceAhead = []                  #same array as above
for i in range(1500):               #but for the look ahead algorithm
    distanceAhead.append([])
    
    
#BUILDING BLOCK FUNCTIONS

def possiblePoints(point,points,noReturn):          #Returns points you can visit from the point
    ans = []                                        #ans is all the possible points, will be updated later
    for diff in (-1,1):                             #difference of +1 or -1
        p = (point[0]+diff,point[1])                #change the first value in point (vertical movement)
        if p not in points and p not in noReturn:   #if this new p isn't in already visited points are points of no return
            ans.append(p)                           #add it to ans
        p = (point[0],point[1]+diff)                #move in the other direction (horizontal movement)
        if p not in points and p not in noReturn:   #check again and add
            ans.append(p)
    return ans                                      #return answers
    
def markNoReturn(points,pointList,noReturn):        #mark points of no return by adding them to noReturn
    lastPoint = pointList[-2]                                       #points of no return are adjacent to previous point
    possibleToMark = possiblePoints(lastPoint,points,noReturn)      #check only points not already marked or taken
    for possible in possibleToMark:                                 #loop through points
        oneAway = (possible[0]*2-lastPoint[0],possible[1]*2-lastPoint[1])       #move one directly away from lastPoint
        for i in range(-2,3):                                                   #i will let us move in other direction
            side = (oneAway[0] + (possible[1]-lastPoint[1])*i,oneAway[1]+i*(possible[0]-lastPoint[0]))  #we need to move in opposite direction as away
            if side in points:                                                                          #move to the side by switching distances
                noReturn.add(possible)                                                                  #if one of these points exsists, mark possible as a point of no return
    #NOTE, the above algorithm isn't perfect, and will have both false positives and negatives, but resulted in a significant improvement over the naive algorithm

#THE WALKING ALGORITHMS

def naiveWalk():
    point = (0,0)                   #starting point
    points = set()                  #store all visited points in set
    points.add(point)               #mark starting point as visited
    pointList = [(0,0)]             #store points visited in an ordered list as well, can be used for visualizing
    while True:
        distanceTraveled = math.hypot(*point)                   #calculate distance traveled from the origin
        distanceNaive[len(points)-1].append(distanceTraveled)   #append it to distances, -1 because we start from length 1
        nextPoints = possiblePoints(point,points,[])            #find the next poitns we can choose from
                                                                #empty list because not considering points of no return
        if not nextPoints:                                      
            break                                               #break if we can't choose from any points
        point = random.choice(nextPoints)                       #choose random points from those free
        pointList.append(point)                                 #add it to the list
        points.add(point)                                       #add point to set
    
    return pointList            #When done, return list of points in order
            
def lookAheadWalk():            #Similar to naive algorithm but tries to predict which points are bad to go to
    point = (0,0)                   #starting point
    points = set()                  #store all visited points in set
    points.add(point)               #mark starting point as visited
    pointList = [(0,0)]             #store points visited in an ordered list as well, can be used for visualizing
    noReturn = set()                #store predicted points of no return, those the algorithm will avoid
    while True:
        distanceTraveled = math.hypot(*point)                   #calculate distance traveled from the origin
        distanceAhead[len(points)-1].append(distanceTraveled)   #append it to distances, -1 because we start from length 1
        nextPoints = possiblePoints(point,points,noReturn)      #find next points we can choose from not taken or points of no return
        if not nextPoints:                                      #if no points here, still consider not taken points but those predicted to be no return
            nextPoints = possiblePoints(point,points,[])        #these points are therefore made a last resort
            if not nextPoints:                                  #if still no points, we are done, so break
                break
        point = random.choice(nextPoints)                       #choose a random point of those avaliable
        pointList.append(point)                                 #add it to list
        points.add(point)                                       #add it to set
        markNoReturn(points,pointList,noReturn)                 #mark points to not visit
    
    return pointList                                            #done, return list


#COLLECTING DATA

lookAheadLengths = []               #Will store lengths from look ahead algorithm
lengthsNaive = []                   #Will store lengths from naive algorithm

for i in range(numIterations):
    lookAheadLengths.append(len(lookAheadWalk()))       #store the legnth for both
    lengthsNaive.append(len(naiveWalk()))

pathLengthNaive = []                #Path lengths from the naive algorithm
avgDistNaive = []                   #Avg distances at each path length for algorithm
for x in range(1500):
    if distanceNaive[x]:            #If we reached this length
        pathLengthNaive.append(x)                       #append pathLength
        avgDistNaive.append(np.mean(distanceNaive[x]))  #append average distance traveled

pathLengthAhead = []                #Path lengths from the look ahead algorithm algorithm
avgDistAhead = []                   #Avg distances at each path length for algorithm
for x in range(1500):
    if distanceAhead[x]:            #If we reached this length
        pathLengthAhead.append(x)                       #append pathLength
        avgDistAhead.append(np.mean(distanceAhead[x]))  #append average distance traveled

#GRAPHS
        
#Histogram of how many steps each algorithm goes for
numBins = 30                #number of bins for naive algorithm
fig = plt.figure()          #some pyplot stuff
ax = fig.add_subplot(111)   
#create scaling factor so histogram bars are about same side
scalingFactor = (max(lookAheadLengths)-min(lookAheadLengths))/(max(lengthsNaive)-min(lengthsNaive))
ax.hist(lookAheadLengths,numBins*scalingFactor, color = 'r',alpha = .5, label = 'Look Ahead')       #plot with some transparency
ax.hist(lengthsNaive,numBins,color = 'b',alpha = .5, label = 'Naive')
legend = ax.legend()                    #create legend
ax.set_xlabel("Length of Path")         #axes labels
ax.set_ylabel("Number of occurences out of {0}".format(numIterations))
fig.show()
plt.show()          #for some reason I need this or the first plot doesn't show

#Print average path lengths
print("Average length of path with naive algorithm is {0}".format(sum(lengthsNaive)/len(lengthsNaive)))
print("Average length of path with look ahead algorithm is {0}".format(sum(lookAheadLengths)/len(lookAheadLengths)))

plt.plot(pathLengthNaive,avgDistNaive,'b',label = 'naive')          #Plot naive distances
plt.plot(pathLengthAhead,avgDistAhead,'g',label = 'look ahead')     #plot look ahead distances
plt.xlabel('Number of steps')                                       #label axes
plt.ylabel('Avg distance traveled')
plt.legend()                                                        #add legend
plt.show()                                                          #show

#graph steps vs distance squared
plt.plot(pathLengthNaive,np.square(avgDistNaive),'b',label = 'naive')           #Plot naive distances
plt.plot(pathLengthAhead,np.square(avgDistAhead),'g',label = 'look ahead')      #plot look ahead distances
plt.xlabel('Number of steps')                                                   #label axes
plt.ylabel('Avg distance traveled squared')
plt.legend()                                                                    #add legend
plt.show() 


#Will do linear regression of all the points combined of log log plots
m,b,r,p,stderr = linregress(np.concatenate((np.log(pathLengthNaive[1:200]),np.log(pathLengthAhead[1:200]))),
                            np.concatenate((np.log(avgDistNaive[1:200]),np.log(avgDistAhead[1:200]))))
#in the above, only used first 200 points because it get's less accurate after there

#log log plot
plt.plot(np.log(pathLengthNaive[1:]),np.log(avgDistNaive[1:]),'b',label = 'naive')           #Plot naive distances
plt.plot(np.log(pathLengthAhead[1:]),np.log(avgDistAhead[1:]),'g',label = 'look ahead')      #plot look ahead distances
plt.plot(np.log(pathLengthNaive[1:]),m*np.log(pathLengthNaive[1:])+b,'r',label = 'regression')
plt.xlabel('log(Number of steps)')                                                   #label axes
plt.ylabel('log(Avg distance traveled)')
plt.legend()                                                                    #add legend
plt.show()

print('''Log log regression of first 200 points is y = {0}*x+{1}
with R^2 of {2}
This indicates that Avg Distance Traveled = {3}*steps^{4}'''.format(
    m,b,r**2,math.exp(b),m))
#Comparison graph, the differences between the algorithms
plt.plot(pathLengthNaive[:200],np.subtract(avgDistAhead[:200],avgDistNaive[:200]),'b')      #Plot difference of distances
plt.xlabel('Number of steps')                                   #label axes                 #only use first 200 points for accuracy
plt.ylabel('Difference  between look ahead and naive')
plt.show() 

