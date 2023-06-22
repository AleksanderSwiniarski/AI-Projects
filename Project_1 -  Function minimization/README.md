#Function minimization

Program optimizes for two to choose from functions:
  1. F(x) = a*x^3 + b*x^2 + c*x + d
  2. G(x) = c + b^T*x + x^T * A * x (where b is a d-dimensional vector, A is positive-definite matrix)
for which user can specify parameters and starting point (scalar number for F(x) and vector for G(x)).
User can also choose one out of three possible stopping conditions:
  1. Maximum number of iterations
  2. Desired value of function to reach
  3. Maximum computation time
And finally user has option to define batch/restart mode where user specifies _n_ number of restarts. Program then will calculate the minimal value _n_ times and its function value and mean values and standard deviation is reported. If user chosen random starting point, for each iteration of batch, starting point will be changed.

All the logic is implemented manually.
