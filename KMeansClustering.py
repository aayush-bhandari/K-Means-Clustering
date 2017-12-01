import numpy as np,sys
import copy
from sklearn.metrics.pairwise import euclidean_distances as ed
import random
#input_file = open("test_data.txt","r")
input_file = open(sys.argv[2],"r")

#print(input_file.read())

cordinates = {}
def preProcess():
    # spliting data line by line and adding to dictionary as Key = Id and Value = (x,y) cordinates
    for line in input_file:
        splited_line = line.split()
        cordinates[int(splited_line[0])] = [float(splited_line[1]), float(splited_line[2])]
    #print(cordinates)
    return cordinates;


#select K Means. Randomly select 5 points as means

def kMeans(k,means):
    for x in range(k):
        id = random.randint(1, len(cordinates))
        means[int(id)] = cordinates[id]
    #print(means)
    return means;



# calculate distance for each point from all means
def predictMean(cordinates, means,predictedCategory):
    for id in cordinates:
        minDistance = 10
        tempMean = 0
        for mean in means:
            distance = (ed([cordinates[id]], [means[mean]]))
            if(distance[0][0]<minDistance):
                minDistance = distance[0][0]
                tempMean = mean
        # assign each point to a mean to which it is closer
        if not tempMean in predictedCategory:
            predictedCategory[tempMean] = [id]
        else:
            predictedCategory[tempMean].append(id)
    return predictedCategory

# Recompute values of means
def recomputeMeans(predictedCategory, means):
    for eachMean in predictedCategory:
        listOfPoints = predictedCategory[eachMean]
        newX =0
        newY =0
        for id in listOfPoints:
            newX = newX + cordinates[id][0]
            newY = newY + cordinates[id][1]
        newX = round(newX/len(listOfPoints),2)
        newY = round(newY/len(listOfPoints),2)
        means[eachMean] = [newX, newY]
    return means

#Calculate sum squared error
def caculateSSE(means,predictedCategory,cordinates):
    sse = 0
    for p in predictedCategory:
        list_points = predictedCategory[p]
        for id in list_points:
            sse = sse + ed([cordinates[id]], [means[p]])
    print("SSE = ",sse[0][0])
    return sse[0][0]


#Main method
def main():
    cordinates = preProcess();
    #k = 5;
    k = int(sys.argv[1])
    means = {}
    means = kMeans(k,means)
    prevMeans = {}
    #Iterate over predecting category and computing means till we converge or we reach max iterations
    for i in range(0,25):
        predictedCategory = {}
        predictedCategory = predictMean(cordinates,means,predictedCategory)
        prevMeans = copy.deepcopy(means)
        means = recomputeMeans(predictedCategory,means)
        # If there are no changes in means cordinates, terminate the loop
        if (prevMeans == means):
            break
    print("Final Category",predictedCategory)

    #outputfile = "out.txt"
    outputfile = sys.argv[3]
    with open(outputfile, 'w') as outfile:
        for mean in predictedCategory:
                outfile.write( (str(mean)+":"+str(predictedCategory[mean]))+'\n')
        outfile.write('\n'+"SSE:"+ str(caculateSSE(means,predictedCategory,cordinates)))

main()