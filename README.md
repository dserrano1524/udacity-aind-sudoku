# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A:
Naked twins is a pair of number/digits in the sudoku sited in two different boxes that belong to at least a same unit (a unit is a row, column, area to which a box belongs.
  Depending on the sudoku restrictions, the diagonals also make part of the units). In the context of this course, we take advantage of this property of a sudoku among the
  constraint propagation technique to remove the digits of the twins from the peers of the units of a box, obtaining an 'easier to solve' sudoku after multiple iterations.
  (more info here http://www.sudokuwiki.org/naked_candidates)

  We take advantage of the elimination and only choice constraints to enforce a new constraint that will get a better grid in each iteration\ recursion. We apply the naked twin
   algorithm by removing the digits from the peers of the identified naked twins multiple times to achieve a more complete grid.
   This can be seen in the combination of the reduce_puzzle and search methods, as reduce_puzzle applies all the constraints (elimination, only choice and naked twins),
   and search calls it multiple times using recursion.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We identify the boxes in the diagonal and include them in the unitlist and peers. As eliminate and only_choice uses this structures. The same happens in naked twins.
As this methods are called in the reduce_puzzle and search methods, the new constraint is satisfied in each iteration, leading to a more complete grid in each recursion \ iteration.
So in this case, the diagonal constraint is satisfied using eliminate, only_choice, naked twins and search methods during multiple iterations, as all of them use the unitlist data.s
