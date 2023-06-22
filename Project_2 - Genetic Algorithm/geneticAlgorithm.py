import numpy as np
import os

class multiDimensionalQuadratic:
    
    def __init__(self, matrixA, vectorB, scalarC, dimensions):
        self.matrixA = matrixA
        self.vectorB = vectorB
        self.scalarC = scalarC
        self.dimensions = dimensions

    def value(self, x):
        return np.dot(np.dot(np.transpose(x),self.matrixA),x) + np.dot(np.transpose(self.vectorB),x) + self.scalarC

class geneticAlgo:

    def __init__(self, populationSize, crossoverProbability, mutationProbability, bitLength):
        self.populationSize = populationSize
        self.crossoverProbability = crossoverProbability
        self.mutationProbability = mutationProbability
        self.bitLength = bitLength

    def twosBitTransfomation(self, vector):

        value = -int(vector[0])*(2 ** (np.shape(vector)[0]-1))
        for i in range(1,np.shape(vector)[0]):
            value += int(vector[i]) * (2 ** ((np.shape(vector)[0]-i-1)))

        return value

    def decoding(self, vector):
        x = np.empty([np.shape(self.bitLength)[0],1], dtype=np.int_)
        for i in range(0,np.shape(self.bitLength)[0]):
            x[i] = self.twosBitTransfomation(vector[np.sum(self.bitLength[:i]):np.sum(self.bitLength[:i+1])])
        return x

    def populationInitialization(self):
        
        population = np.zeros([self.populationSize, np.sum(self.bitLength)], dtype = bool)

        for bit in np.nditer(population, op_flags=['readwrite']):
            if np.random.uniform(0,1) <= 0.5:
                bit[...] = not bit[...]
        
        return population

    def rate(self, func, population):

        grades = np.empty([self.populationSize,1], dtype=np.longdouble)
        iter = 0
        for score in np.nditer(grades, op_flags=['readwrite']):
            score[...] = func.value(self.decoding(population[iter][:]))
            iter += 1

        return grades
      
    def reproduction(self, population, grades, age):
        
        # Checking if all of the individuals have the same genotypes to prevent division by zero
        if((np.max(grades) - np.min(grades)) < np.finfo(np.longdouble).eps):
            return population

        parents = np.empty([self.populationSize,np.sum(bitLength)], dtype=bool)
        scaled = np.empty([self.populationSize], dtype=np.longdouble)
        probability = np.empty([self.populationSize], dtype=np.longdouble)

        # Scaling
        iter = 0
        for value in np.nditer(grades, op_flags=['readwrite']):
            scaled[iter] = (value[...] - np.min(grades))/(np.max(grades) - np.min(grades))
            iter += 1

        sum = np.sum(scaled)

        iter = 0
        for prob in np.nditer(probability, op_flags=['readwrite']):
            prob[...] = scaled[iter]/sum
            iter += 1

        for i in range(0,self.populationSize):
            relativeAge = np.random.choice(range(0,self.populationSize), 1, replace=True, p=probability)
            parents[i][:] = population[relativeAge][:]
            age[i] = relativeAge
        return parents

    def geneticOperations(self, population, parents, age):

        offsprings = np.empty([self.populationSize,np.sum(self.bitLength)], dtype=bool)
        np.sort(age)

        number_of_children = 0

        for iter in range(0, self.populationSize-1, 2):
            parent_one = parents[iter][:]
            parent_two = parents[iter+1][:]
            
            if np.random.uniform(0,1) <= self.crossoverProbability:

                cross_point = np.random.randint(1,(np.sum(self.bitLength)-1))
                first_child = np.append(parent_one[:cross_point],parent_two[cross_point:])
                second_child = np.append(parent_two[:cross_point],parent_one[cross_point:])

                offsprings[number_of_children][:] = first_child
                number_of_children += 1
                offsprings[number_of_children][:] = second_child
                number_of_children += 1

        iter2 = 0
        for iter in range(number_of_children, self.populationSize):
            offsprings[iter][:] = population[age[iter2]][:]
            iter2 += 1
                  
        for genome in np.nditer(offsprings, op_flags=['readwrite']):
            if np.random.uniform(0,1) <= self.mutationProbability:
                genome[...] = not genome[...]

        return offsprings

# Choice of parameters for G(x)
# dimensions

print("Program analysing the maximum of G(x) = c + (b^T)x + (x^T)Ax \n")

while True: 
    try:
        dimension = int(input("Choose the dimensions of Matrix and Vector's length: "))
        if dimension <= 0:
            print("Matrix dimensions must be positive!")
        else:
            break
    except ValueError:
        print("Invalid input!")

# Matrix A
    
print(f"Input values of {dimension}x{dimension} matrix")
A = np.empty([dimension,dimension])
index = 1
for value in np.nditer(A, op_flags=['readwrite']):
    while True: 
        try:
            value[...] = float(input(f"Choose the parameter for nr.{index} element: "))
            break
        except ValueError:
            print("Invalid input!")
    index += 1

# Vector b

print(f"Input values of b vector")
b = np.empty([dimension,1])
index = 1
for value in np.nditer(b, op_flags=['readwrite']):
    while True:
        try:
            value[...] = float(input(f"Choose the parameter of nr.{index} element: "))
            break
        except ValueError:
            print("Invalid input!")
    index += 1

# Scalar c

while True:
    try:
        c = float(input("Choose the value of the scalar c: "))
        break
    except ValueError:
        print("Invalid input!")
    
quadratic = multiDimensionalQuadratic(A,b,c,dimension)

# Range of searched integers

bitLength = np.empty([dimension,1], dtype = int)
index = 1

for value in np.nditer(bitLength, op_flags=['readwrite']):
    while True:
        try:
            value[...] = int(input(f"Choose the d parameter to specify range of a searched integer (-2^d <= x < 2^d) in dimension {index}: ")) + 1
            if value[...] < 0:
                print("Please, choose a non-negative number!")
            else:
                break
        except ValueError:
            print("Invalid input!")
    index += 1

# Algorithm parameters

# Population size

while True:
    try:
        populationSize = int(input(f"Choose the size of the population: "))
        if populationSize < 1:
            print("Population size must be positive!")
        else:
            break
    except ValueError:
        print("Invalid input!")

# Crossover probability

while True:
    try:
        crossoverProbability = float(input(f"Choose the probability of crossover (Range: 0 - 1): "))
        if crossoverProbability < 0 or crossoverProbability > 1:
            print("Crossover probability must be chosen from the given range!")
        else:
            break
    except ValueError:
        print("Invalid input!")

# Muatation probability

while True:
    try:
        mutationProbability = float(input(f"Choose the probability of mutatation (Range: 0 - 1): "))
        if mutationProbability < 0 or mutationProbability > 1:
            print("Mutation probability must be chosen from the given range!")
        else:
            break
    except ValueError:
        print("Invalid input!")

genAlgo = geneticAlgo(populationSize, crossoverProbability, mutationProbability, bitLength)

# No. of Iterations

while True:
    try:
        iterations = int(input(f"Choose the number of iterations of algorithm: "))
        if iterations < 1:
            print("Iteration number must be positive!")
        else:
            break
    except ValueError:
        print("Invalid input!")

# Evolutionary algorithm

iter = 0
ages = np.empty([populationSize], dtype=np.int_)
population = genAlgo.populationInitialization()
grades = genAlgo.rate(quadratic, population)
while iter < iterations:
    parents = genAlgo.reproduction(population, grades, ages)
    offsprings = genAlgo.geneticOperations(population, parents, ages)
    grades = genAlgo.rate(quadratic, offsprings)
    population = offsprings
    iter += 1

print("Final population: \n")
for i in range(0, genAlgo.populationSize):
    print(f"Individual nr.{i+1}: {population[i][:]}, grade: {grades[i]}\n")
print(f"Maximized number: {np.max(grades)}")

os.system('pause')