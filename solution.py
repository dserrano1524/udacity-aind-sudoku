assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    result = []
    for c in A:
        for ch in B:
            result.append(c + ch)
    return result

# This method  receives rows 'ABCDEFGHI' and columns '123456789'
def get_diagonal(rows, columns):
    """
    Cross rows and columns on an iteration to obtain the diagonal
    Input: Rows = 'ABCDEFGHI' and columns = '123456789'
    Output: List of diagonal boxes
    """
    diagonal_boxes = []
    for i in range(len(rows)):
        diagonal_boxes.append(rows[i] + columns[i])
    return diagonal_boxes
# This method  receives rows 'ABCDEFGHI' and columns '123456789'
def get_inv_diagonal(rows, columns):
    """
    Cross rows and columns on an iteration to obtain the diagonal
    Input: Rows = 'ABCDEFGHI' and columns = '123456789'
    Output: List of inverteddiagonal boxes
    """
    diagonal_boxes = []
    j = len(rows) - 1
    for i in range(len(rows)):
        diagonal_boxes.append(rows[i] + columns[j])
        j = j - 1
    return diagonal_boxes
"""
Support structures for code
"""

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = get_diagonal(rows, cols)
inv_diagonal_units = get_inv_diagonal(rows, cols)
unitlist = row_units + column_units + square_units + [diagonal_units] + [inv_diagonal_units]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Algorithm: For each unit, search digit values where their lenght is equal to 2
    and add them to a dictionary (grouping equal twin candidates). Then, iterate
    over twins and map the digits to remove to the units where they must be removed
    then remove digits form units. As we iterate over units and not peers, avoid
    removing digits from naked peers.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # Contains K: digits, V: boxes that containg digits
        naked_candidates = {}
        for box in unit:
            digits = values[box]
            if(len(digits)) == 2:
                if digits in naked_candidates:
                    # Gives pairs of boxes with same digits
                    naked_candidates[digits].append(box)
                else:
                    naked_candidates[digits] = [box]
        # Contains K: digits V: units where digits will be eliminated
        # We want to identify the units where digits must be removed
        naked_twins = {}
        for k in naked_candidates:
            if len(naked_candidates[k]) == 2:
                if k in naked_twins:
                    naked_twins[k].append(unit)
                else:
                    naked_twins[k] = [unit]

        for digits in naked_twins:
            for unit in naked_twins[digits]:
                for box in unit:
                    #Avoid removing digits from other naked twin
                    if values[box] not in digits:
                        # We remove all digits from units, except from twins (peers by definition)
                        # We do this over units rather than peers to evaluate the diagonal easily
                        for d in digits:
                            assign_value(values, box, values[box].replace(d,''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    arr = []
    for ch in grid:
        if ch == '.':
            arr.append('123456789')
        else:
            arr.append(ch)
    return dict(zip(boxes, arr))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    one_digit_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in one_digit_boxes:
        single_value = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(single_value, '')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # TODO Add Naked Twins to algorithm
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

# This method shall only be used  when values is a sudoku that contains
# boxes as keys and strings containing number as values. No blanks
def find_min_box(values):
    """
    Method thta returns the box with the min amount of digits in the values dict
    Input: Rows = 'ABCDEFGHI' and columns = '123456789'
    Output: List of diagonal boxes
    """
    # Max value in a box can be 123456789
    min_box = None
    min_value = '123456789'
    for box, digits in values:
        if len(digits) > 1 and len(digits) < len(min_value):
            min_value = digits
            min_box = box
    return min_box

def search(values):
    """Using depth-first search and propagation, try all possible values.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form."""
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Choose the box with the min vlaeu
    s = find_min_box(values)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
