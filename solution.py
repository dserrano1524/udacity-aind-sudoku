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
    diagonal_boxes = []
    for i in range(len(rows)):
        diagonal_boxes.append(rows[i] + columns[i])
    return diagonal_boxes
# This method  receives rows 'ABCDEFGHI' and columns '123456789'
def get_inv_diagonal(rows, columns):
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

def naked_twins_fail(values):
    # NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Candidate twins are boxes where digits length are size 2
    candidate_twins = [box for box in values.keys() if len(values[box]) == 2]
    # We create a dictionary that will contain our naked twins
    naked_twins = {}
    # We map digits to pairs of twins
    for box in candidate_twins:
        digits = values[box]
        # If we arleady have the same digits in a box, we append a new box
        if digits in naked_twins:
            naked_twins[digits].append(box)
        # If we don't have the k,v, we add it
        else:
            naked_twins[digits] = [box]
    # We only use naked twins were we grouped exactly 2 naked twins
    for dig, boxes in naked_twins:
        # We only wnat pairs of boxes of 2 digits, not single boxes of 1 digit
        if(len(boxes) == 2):
            print('this are my boxes', boxes)
            # We take the units of each naked twins to remove the digits
            units_nt1 = [item for sublist in units[boxes[0]] for item in sublist]
            units_nt2 = [item for sublist in units[boxes[1]] for item in sublist]
            all_units = set(units_nt1) & set(units_nt2)
            # We check the diagonals too
            if box[0] in diagonal_units or box[1] in diagonal_units:
                all_units = all_units & set(diagonal_units)
            if box[1] in diagonal_units or box[1] in inv_diagonal_units:
                all_units = all_units & set(diagonal_units)
            # We only want to remove the digits from the intersection of the units
            for box in all_units:
                if len(values[box])>2:
                    # Now we remove each digit of the naked twin
                    #print(peer_box)
                    for d in dig:
                        #print(digit)
                        peer_digits = values[box]
                        peer_digits.replace(d, '')
                        values = assign_value(values, box, peer_digits)


def naked_twins_fail2(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Candidate twins are boxes where digits lenght are size 2
    candidate_twins = [box for box in values.keys() if len(values[box]) == 2]
    #print('candidates', candidate_twins)

    naked_twins_array = []
    for box in candidate_twins:
        candidate_peers = peers[box]
        for box_cp in candidate_peers:
            if values[box] == values[box_cp]:
                naked_twins_array.append([box, box_cp])
    #print(naked_twins_array)
    for naked_twin_tuple in naked_twins_array:
        print(naked_twin_tuple)
        nt1_box = naked_twin_tuple[0]
        #print(nt1_box)
        nt2_box = naked_twin_tuple[1]
        # We get the peers of the naked twins
        peers_nt1 = [item for sublist in units[nt1_box] for item in sublist]
        peers_nt2 = [item for sublist in units[nt2_box] for item in sublist]
        #print('cosa: ', peers_nt1)
        # We want to remove the digits form the intersection of the unique pairs of the naked twins
        # We only want to modify the peers they share, so we get the intersection
        all_peers = set(peers_nt1) & set(peers_nt2)
        #print('all_peers', all_peers)
        for peer_box in all_peers:
            # We check if the box has more than 1 digit
            if len(values[peer_box])>2:
                # Now we remove each digit of the naked twin
                #print(peer_box)
                for digit in values[peer_box]:
                    #print(digit)
                    peer_digits = values[peer_box]
                    peer_digits.replace(digit, '')
                    values = assign_value(values, peer_box, peer_digits)
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
    one_digit_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in one_digit_boxes:
        single_value = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(single_value, '')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
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
    # Max value in a box can be 123456789
    min_box = None
    min_value = '123456789'
    for box, digits in values:
        if len(digits) > 1 and len(digits) < len(min_value):
            min_value = digits
            min_box = box
    return min_box

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
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
