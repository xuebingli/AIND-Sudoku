DIGITS = '123456789'
ROWS = 'ABCDEFGHI'
COLS = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

def in_three(items):
    return [items[i:i+3] for i in range(0, len(items), 3)]

SQUARES = cross(ROWS, COLS)
TOP_DIAGONAL = list(filter(lambda s: ROWS.index(s[0]) == COLS.index(s[1]), SQUARES))
BOTTOM_DIAGONAL = list(filter(lambda s: ROWS.index(s[0]) + COLS.index(s[1]) == 8, SQUARES))
COLS_IN_THREE = in_three(COLS)
ROWS_IN_THREE = in_three(ROWS)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

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
    possibility_grid = [DIGITS if d == '.' else d for d in list(grid)]
    return dict(zip(SQUARES, possibility_grid))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    values_list = sorted(list(values.items()))
    digits_list = [ds for _, ds in values_list]
    rows = [digits_list[i: i + 9] for i in range(0, 81, 9)]
    for row in rows:
        for digits in row:
            print('%-10s' % (digits), end='')
        print()

def eliminate(values):
    for s in values.keys():
        for p in peers(s):
            if len(values[p]) == 1: # the peer is solved
                assign_value(values, s, values[s].replace(values[p], ''))
    return values

def peers(square):
    """
    Find all peers for a given square.
    """
    row, col = square
    in_same_row = [row + c for c in COLS]
    in_same_col = [r + col for r in ROWS]
    in_same_unit = unit_of_square(square)
    peers = in_same_row + in_same_col + in_same_unit
    if square in TOP_DIAGONAL:
        peers += TOP_DIAGONAL
    elif square in BOTTOM_DIAGONAL:
        peers += BOTTOM_DIAGONAL
    return list(set(filter(lambda s: s != square, peers))) # remove the square itself and duplicates

def unit_of_square(square):
    row, col = square
    rows = next(rows for rows in ROWS_IN_THREE if row in rows)
    cols = next(cols for cols in COLS_IN_THREE if col in cols)
    return cross(rows, cols)

def only_choice(values):
    for s in values.keys():
        unit = unit_of_square(s)
        unit_digits = map(lambda s: values[s], unit)
        all_digits_in_unit = ''.join(unit_digits)
        for d in values[s]:
            if all_digits_in_unit.count(d) == 1: # digit only appears once in unit
                assign_value(values, s, d)
    return values

def solved_square_count(values):
    return len([s for s, ds in values.items() if len(ds) == 1])

def is_unsolvable(values):
    return any(len(ds) == 0 for ds in values.values())

def reduce_puzzle(values):
    keep_reducing = True
    while keep_reducing:
        solved_square_count_before = solved_square_count(values)
        values = eliminate(values)
        values = only_choice(values)
        solved_square_count_after = solved_square_count(values)
        keep_reducing = solved_square_count_before < solved_square_count_after
    return values

def is_solved(values):
    return all(len(ds) == 1 for ds in values.values())

def unsolved_square_with_least_possibilities(values):
    _, square = min([(len(ds), s) for s, ds in values.items() if len(ds) > 1])
    return square

def search(values):
    values = reduce_puzzle(values)
    if is_solved(values): return values
    elif is_unsolvable(values): return False
    else:
        s = unsolved_square_with_least_possibilities(values)
        for d in values[s]:
            possible_values = values.copy()
            assign_value(possible_values, s, d)
            answer_values = search(possible_values)
            if answer_values: return answer_values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

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
