import random,math,time

#set constants
POPULATIONSIZES={10,100,500,1000}
MUTATIONFACTOR=50
MAXPERFORMANCE=56

#initialize variables
NumIterations = 100
statsFile= open("stat.csv","w")

#define classes
class Solution:

    def __init__(self):
        workingList = [1,2,3,4,5,6,7,8]
        self.data = []
        while len(workingList)>0:
            self.data.append(workingList.pop(random.randint(0,len(workingList)-1)))
        self.performance = MAXPERFORMANCE
        self.measurePerformance()
        #print(str(self.data) + " scored "+str(self.performance))
        del workingList
        return

    def ManualSet(self,listIn:list):
        #check incoming list for errors
        if len(listIn)!=8:
            raise Exception(str(len(listIn))+" elements provided, and 8 are required for creating a solution")
        for element in {1,2,3,4,5,6,7,8}:
            if listIn.count(element)!=1:
                raise Exception(str(len(listIn))+" elements provided, and 8 are required for creating a solution")
        self.data = listIn.copy()
        self.performance = MAXPERFORMANCE
        self.measurePerformance()
        #print(str(self.data) + " scored "+str(self.performance))
        return
    
    def measurePerformance(self):
        
        for currentQueen in self.data:
            #check columns for other attacking Queens
            #not needed since each queen has their own column
            #check rows for attacking Queens
            #testing has shown that gene splicing errors do not occur, thus this isn't needed
            #if self.data.count(currentQueen)>1:
            #    self.performance = 0
            #    print ("gene splicing error, discard")
            #    return
            #check diaganols
            #this is kinda hard, what we need to do is check all other indices
            #and ensure that they are not equal to the value of the current number +/-
            #the difference in indices
            for otherQueens in self.data:
                #first check to make sure we are not comparing against our currentQueen
                if self.data.index(otherQueens) == self.data.index(currentQueen):
                    continue
                indexDifference = abs(self.data.index(otherQueens) - self.data.index(currentQueen))
                if (otherQueens+indexDifference == currentQueen) or ((otherQueens-indexDifference == currentQueen)):
                    self.performance-=1
        return

    def DisplaySolution(self):
        for row in range (0,8):
            display = ["_","_","_","_","_","_","_","_"]
            display[self.data.index(8-row)]="Q"
            print(display)



#define functions
def PerformanceSort(thisSolution):
    return thisSolution.performance

def GatherStats(populationToAnalyze:list) -> list:
    leastPerformance=MAXPERFORMANCE
    bestPerformance=0
    averagePerformance=0
    for currentSolution in populationToAnalyze:
        if currentSolution.performance < leastPerformance:
            leastPerformance = currentSolution.performance
        if currentSolution.performance > bestPerformance:
            bestPerformance = currentSolution.performance
        averagePerformance+=currentSolution.performance
    averagePerformance=averagePerformance/len(populationToAnalyze)
    return [leastPerformance,bestPerformance,averagePerformance,time.time()]



#begin program
for populationSize in POPULATIONSIZES:
    print("population size "+str(populationSize)+" with "+str(NumIterations)+" iterations.")
    
    #create initial populzation of random solutions
    population=[Solution() for _ in range(populationSize)]
    #create inital stats list
    stats = []

    #sort by performance score
    population.sort(reverse=False,key=PerformanceSort)

    #gather initial stats
    stats.append(GatherStats(population))

    #begin GA iterations
    for iteration in range(0,NumIterations):
        print(str(iteration),end =",")

        #create new population
        newGeneration = []
        #newGenIndex = 0
        #I got tired of the GA killing off good solutions
        #so I updated this section to copy forward any existing
        #solutions before performing any GA calcs, this also
        #trims out duplicate solutions per generation to reduce
        #overall duplicate population while also setting up 
        ##the normalization factor
        normFactor=0
        for currentSolution in population:
            normFactor+=currentSolution.performance
            if currentSolution.performance == MAXPERFORMANCE:
                dupeFlag = True
                for comparisonSolution in newGeneration:
                    if str(currentSolution.data)==str(comparisonSolution.data):
                        dupeFlag = False
                        break
                if dupeFlag:
                    newGeneration.append(currentSolution)
                #newGenIndex+=1
            
        #time to make a new generation
        #while new generations size is less than current population size
        while len(newGeneration) < populationSize:
            #find two parents, weighted for better performance scores
            weight = random.randint(0,normFactor)
            parent1 = None
            for currentSolution in population:
                weight -= currentSolution.performance
                if weight <= 0:
                    parent1=currentSolution
                    break
            #make sure parent1 got assigned
            if parent1 == None:
                print("Parent 1 did not get assigned!!")
                print("normFactor = "+str(normFactor)+" weight = "+str(weight)+" and current solution is "+str(currentSolution.data))
                continue
            weight = random.randint(0,normFactor)
            parent2 = None
            for currentSolution in population:
                weight -= currentSolution.performance
                if weight <= 0:
                    parent2=currentSolution
                    break
            #make parent2 got assigned
            if parent2 == None:
                print("Parent 2 did not get assigned!!")
                print("normFactor = "+str(normFactor)+" weight = "+str(weight)+" and current solution is "+str(currentSolution.data))
                continue
            #Choose a locus on parent1
            #I prefer to make it based on the performance of the parent
            #in this case, I randomly select a locus point with a range
            #dictated by the perforamnce, where best perforamnce allows
            #for a locus  up to largest index, and worst allows only
            #the smallest
            maxIndex=math.floor((len(parent1.data)-1)-(((MAXPERFORMANCE-parent1.performance)/MAXPERFORMANCE)*(len(parent1.data)-1)))
            childData=[]
            for currentNum in range(0,random.randint(0,maxIndex)):
                childData.append(parent1.data[currentNum])
            #now that we have parent1's contribution, we fill the rest
            #by iterating over parent2, and appending the current number
            #only if it is not present in child
            for currentNum in parent2.data:
                if childData.count(currentNum)<1:
                    childData.append(currentNum)
            #now we need to check if this child needs mutation
            while random.randint(0,100) > MUTATIONFACTOR:
                #this child has been chosen for mutation
                #select 1 index at random
                index1 = random.randint(0,len(childData)-1)
                #select another index at random
                index2 = random.randint(0,len(childData)-1)
                #if both indices are equal, try again
                if index1 == index2:
                    continue
                else:
                    #swap elements at these indices
                    temp = childData[index1]
                    childData[index1]=childData[index2]
                    childData[index2]=temp
                    del temp
            #now we add this new child to the new generation
            try:
                newGeneration.append(Solution())
                newGeneration[-1].ManualSet(childData)
                #newGeneration[newGenIndex].ManualSet(childData)
                #newGenIndex+=1
            except Exception as e: 
                print("Child failed to generate because:"+str(e))
        #now that we have made a new generation
        #we replace the old population with the new population
        population = newGeneration.copy()
        #population.sort(reverse=False,key=PerformanceSort)
        del newGeneration
        #be sure to regather stats
        stats.append(GatherStats(population))
    print("complete!")
    #sort by performance score
    population.sort(reverse=True,key=PerformanceSort)

    #display our final results
    #for currentSolution in population:
    #    print("solution "+str(currentSolution.data)+" has performance score of "+str(currentSolution.performance))
    #    if currentSolution.performance == MAXPERFORMANCE:
    #        currentSolution.DisplaySolution()
    statsFile.write("population size "+str(populationSize)+" with "+str(NumIterations)+" iterations\n")
    statsFile.write("Generation,Least Performance,Best Performance,Average Performance,Time per Generation\n")
    statCounter=0
    totalTime=0
    for stat in stats:
        if stats.index(stat) == 0:
            print("Generation:"+str(statCounter)+" Least Performance:"+str(stat[0])+" Best Performance:"+str(stat[1])+" Average Performance:"+str(stat[2]))
            statsFile.write(str(statCounter)+","+str(stat[0])+","+str(stat[1])+","+str(stat[2])+"\n")
        else:
            perTime=stat[3]-stats[statCounter-1][3]
            totalTime+=perTime
            print("Generation:%d Least Performance:%d Best Performance:%d Average Performance:%f time per generation:%1.4f"%(statCounter,stat[0],stat[1],stat[2],perTime))
            statsFile.write(str(statCounter)+","+str(stat[0])+","+str(stat[1])+","+str(stat[2])+","+str(perTime)+"\n")
        statCounter+=1
    averageTime=totalTime/(len(stats)-1)
    print("average time per generation:"+str(averageTime)+" seconds")
    del stats
    del population

#clean up
statsFile.close()