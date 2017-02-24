# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We take advantage of the elimination and only choice constraints to enforce a new constraint that will get a better grid in each iteration\ recursion. We apply the naked twin
   algorithm by removing the digits from the peers of the identified naked twins multiple times to achieve a more complete grid.
   This can be seen in the combination of the reduce_puzzle and search methods, as reduce_puzzle applies all the constraints (elimination, only choice and naked twins),
   and search calls it multiple times using recursion.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We identify the boxes in the diagonal and include them in the unitlist and peers. As eliminate and only_choice uses this structures. The same happens in naked twins. As this methods are called in the reduce_puzzle and search methods, the new constraint is satisfied in each iteration, leading to a more complete grid in each recursion \ iteration.
