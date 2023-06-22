#Genetic Algorithm

The program analyses function F(x) = x^T * A * x + b^T * x + c and provides information about integer number that maximizes it.
Program also returns information about the last population and targer function values of each member.

Implementation contains:
  - Roultette-wheel selection with scaling
  - Single point crossover
  - FIFO replacement strategy
  - Genetic algorithm uses binary vectors

User can specify:
  - The problem dimensionality
  - The range of seacrched integers as d >= 1 that for each dimension i, -2^d <= x_i < 2^d
  - Function parameters: A, b, c
  - The algorithm parameters as: population size, corssover probability, mutation probability, number of iterations
(User provided parameters are validated by the program)
