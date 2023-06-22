import numpy as np
import time
import os

class Function:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

class F(Function):

    def value(self, x):
        return float(self.a)*(float(x) ** 3) + float(self.b)*(float(x) ** 2) + float(self.c)*float(x) + float(self.d)

    ## First derivative

    def dF(self, x):
        return float(self.a)*3*(float(x) ** 2) + float(self.b)*2*float(x) + float(self.c)

    ## Second derivative

    def ddF(self,x):
        return float(self.a)*6*float(x) + float(self.b)*2
    
    def newtons(self, x):
        return x - self.dF(x)/self.ddF(x)
        
    def gradient(self, x):
        return x - learning_rate*self.dF(x)

class G(Function):

    def value(self, x):
        return np.dot(np.dot(np.transpose(x),self.a),x) + np.dot(np.transpose(self.b),x) + self.c

    ## Gradient

    def dG(self, x):
        dg = np.zeros([self.d,1])
        for i in range(0, self.d):
            dg[i] += self.b[i]
            
            for n in range(0,self.d):
                dg[i] += self.a[i][n]*x[n]
            
            for n in range(0,self.d):
                dg[i] += self.a[n][i]*x[n]

        return dg

    ## Hessian

    def ddG(self,x):
        ddg = np.zeros([self.d,self.d])

        for i in range(0,self.d):
            for n in range(0,self.d):
                ddg[i][n] += self.a[i][n] + self.a[n][i]

        return ddg

    def newtons(self, x):
        return np.subtract(x, np.dot(np.linalg.inv(self.ddG(x)), self.dG(x)))

    def gradient(self, x):
        return np.subtract(x, learning_rate*self.dG(x))

def stopCondition(chosen_stopping_condition, stopping_condition, iterations, value, time):
    match chosen_stopping_condition:
        case 1: ## Max iterations
            if iterations < stopping_condition:
                return True
        case 2: ## Desired Value
            if  stopping_condition < value:
                return True
        case 3: ## Max comp. time
            if time < stopping_condition:
                return True
    return False

## Choice of method

while True: 
    try:
        chosen_method = int(input("Choose the method of minimalization:\n 1: Gradient descent method    2: Newton's method \n"))
        if chosen_method == 1 or chosen_method == 2:
            break
        else:
            print("Not one of the options!")
    except ValueError:
        print("Invalid input!")

match chosen_method:
    case 1:
        while True: 
            try:
                learning_rate = float(input("Choose the learing rate of the method: "))
                if learning_rate > 0:
                    break
                else:
                    print("Learning rate must be positive number!")
            except ValueError:
                print("Invalid input!")
        method = 'gradient'
    case 2:
        method = 'newtons'
    
## Choice of Function 

while True: 
    try:
        chosen_function = int(input("Choose the function for minimalization:\n 1: F(x) = ax^3 + bx^2 + cx + d    2: G(x) = c + (b^T)x + (x^T)Ax \n"))
        if chosen_function == 1 or chosen_function == 2:
            break
        else:
            print("Not one of the options!")
    except ValueError:
        print("Invalid input!")

match chosen_function:
    case 1:
        
        ## Choice of parameters for F(x): a,b,c,d
        
        var = ['a','b','c','d']
        print("Choose the values of variables:")
        for i in range(0, len(var)):
            while True:
                try:
                    var[i] = float(input(f"   {var[i]}:"))
                    break
                except ValueError:
                    print("Invalid input!")
                    
        func = F(var[0], var[1], var[2], var[3])

    case 2:

        # Choice of parameters for G(x)
        # dimensions
        
        while True: 
            try:
                matrix_dimension = int(input("Choose dimensions of Vector/Matrix: "))
                if matrix_dimension <= 0:
                    print("Matrix dimensions must be positive!")
                else:
                    break
            except ValueError:
                print("Invalid input!")

        # Matrix A
        
        print(f"Input values of {matrix_dimension}x{matrix_dimension} matrix")
        A = np.empty([matrix_dimension,matrix_dimension])
        index = 1
        for value in np.nditer(A, op_flags=['readwrite']):
            while True: 
                try:
                    value[...] = float(input(f"Choose the parameter for nr.{index} element:"))
                    break
                except ValueError:
                    print("Invalid input!")
            index += 1

        # Vector b

        print(f"Input values of b vector")
        b = np.empty([matrix_dimension,1])
        index = 1
        for value in np.nditer(b, op_flags=['readwrite']):
            while True:
                try:
                    value[...] = float(input(f"Choose the parameter of nr.{index} element:"))
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
        
        func = G(A,b,c,matrix_dimension)

## Choice of batch/restart mode

while True:
    try:
        number_of_batches = int(input("Choose the batch/restard mode:\n 1: No restarts    2: With restarts \n"))
        match number_of_batches:
            case 1:
                break
            case 2:
                while True:
                    try:
                        number_of_batches = int(input("Choose the number of batches: "))
                        if number_of_batches <= 1:
                            print("Number of batches must be positive!")
                        else:
                            break
                    except ValueError:
                        print('Invalid input!')
                while True: 
                    try:
                        low = float(input("Input lower bound of range of random numbers: "))
                        break
                    except ValueError:
                            print("Invalid input!")
                while True: 
                    try:
                        high = float(input("Input upper bound of range of random numbers: "))
                        break
                    except ValueError:
                        print("Invalid input!")
                break
            case _:
                print("Not one of the options!")
    except ValueError:
        print('Invalid input!')

## Choice of starting point

if(number_of_batches == 1):
    while True: 
        try:
            starting_choice = int(input("Way of choosing starting point:\n 1: Specified value     2: Randomly generated  \n"))
            if starting_choice == 1 or starting_choice == 2:
                break
            else:
                print("Not one of the options!")
        except ValueError:
            print("Invalid input!")

    match chosen_function:
        case 1:
            match starting_choice:
                case 1:
                    while True: 
                        try:
                            x = float(input("Input value of starting point: "))
                            break
                        except ValueError:
                            print("Invalid input!")
                case 2:
                    while True: 
                        try:
                            low = float(input("Input lower bound of range of random numbers: "))
                            break
                        except ValueError:
                            print("Invalid input!")
                    while True: 
                        try:
                            high = float(input("Input upper bound of range of random numbers: "))
                            break
                        except ValueError:
                            print("Invalid input!")
                    x = np.random.uniform(low, high)
        case 2:
            x = np.empty([matrix_dimension,1])
            match starting_choice:
                case 1:
                    index = 1
                    for value in np.nditer(x, op_flags=['readwrite']):
                        while True:
                            try:
                                x[...] = float(input(f"Choose {index} value of vector: "))
                                break
                            except ValueError:
                                print("Invalid input!")
                        index += 1
                case 2:
                    while True: 
                        try:
                            low = float(input("Input lower bound of range of random numbers: "))
                            break
                        except ValueError:
                            print("Invalid input!")
                    while True: 
                        try:
                            high = float(input("Input upper bound of range of random numbers: "))
                            break
                        except ValueError:
                            print("Invalid input!")
                    for val in np.nditer(x, op_flags=['readwrite']):
                        val[...] = np.random.uniform(low, high)

## Choice of stopping condition

while True:
    try:
        chosen_stopping_condition = int(input("Choose the stopping condition:\n 1: Maximum number of iterations     2: Desired value     3: Maximum computation time\n"))
        if chosen_stopping_condition == 1 or chosen_stopping_condition == 2 or chosen_stopping_condition == 3:
            break
        else:
            print("Not one of the options!")
    except ValueError:
        print("Invalid input!")

## Adjusting the stopping condition

match chosen_stopping_condition:
    case 1:
        while True:
            try:
                stopping_condition = int(input("Choose the maximum number of iterations: "))
                if stopping_condition <= 0:
                        print("Number of iterations must be positive!")
                else:
                    break
            except ValueError:
                print("Invalid input!")
    case 2:
        while True:
            try:
                stopping_condition = float(input("Choose the desired value: "))
                break
            except ValueError:
                print("Invalid input!")
    case 3:
        while True:
            try:
                stopping_condition = int(input("Choose the maximum computation time (in seconds): "))
                if stopping_condition <= 0:
                    print("Time must be positive!")
                else:
                    break
            except ValueError:
                print("Invalid input!")

result = []
iter = 0

## Main Loop
for batches in range(0,number_of_batches):
    ## Generating random vector/scalar number for each batch
    if number_of_batches != 1:
        match chosen_function:
            case 1:
                x = np.random.uniform(low,high)
            case 2:
                x = np.empty([matrix_dimension,1])
                for val in np.nditer(x, op_flags=['readwrite']):
                    val[...] = np.random.uniform(low,high)
    start_time = time.time()
    ## Loop of minimalization method
    while stopCondition(chosen_stopping_condition, stopping_condition, iter, func.value(x), time.time() - start_time):
        x = func.__getattribute__(method)(x)       
        iter += 1
    result.append(x)

print(f"Found minimalized x*: \n {sum(result)/len(result)}")

print(f"Value of function at x*: \n {func.value(sum(result)/len(result))}")

## Standard deviation in case of batches
if number_of_batches != 1:
    print(f"Standard deviation: {np.std(result)}")

os.system('pause')