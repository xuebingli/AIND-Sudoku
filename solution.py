DIGITS = '123456789'
ROW_LETTERS = 'ABCDEFGHI'
COL_DIGITS = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

def in_three(items):
    return [items[i:i+3] for i in range(0, len(items), 3)]

COL_DIGITS_IN_THREE = in_three(COL_DIGITS)
ROW_LETTERS_IN_THREE = in_three(ROW_LETTERS)

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

def are_twins(s1, s2):
    # The two squares are on the same row, same column, or the same territory
    return s1[0] == s2[0] or s1[1] == s2[1] or in_same_territory(s1, s2)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    two_digits_squares = [s for s, ds in values.items() if len(ds) == 2]
    naked_twins = [(t1, t2) for t1 in two_digits_squares for t2 in two_digits_squares
                   if t1 > t2 and values[t1] == values[t2] and are_twins(t1, t2)]
    # Eliminate the naked twins as possibilities for their peers
    for (t1, t2) in naked_twins:
        overlapping_peers = [p1 for p1 in peers(t1) for p2 in peers(t2) if p1 == p2]
        for p in overlapping_peers:
            assign_value(values, p, ''.join([d for d in values[p] if d not in values[t1]]))
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
    possibility_grid = [DIGITS if d == '.' else d for d in list(grid)]
    squares = cross(ROW_LETTERS, COL_DIGITS)
    return dict(zip(squares, possibility_grid))

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

def solved_squares(values):
    return [s for s, ds in values.items() if len(ds) == 1]

def eliminate(values):
    solved = solved_squares(values)
    for s in solved:
        improvable_peers = [p for p in peers(s) if values[s] in values[p]]
        for p in improvable_peers:
            assign_value(values, p, values[p].replace(values[s], ''))
    return values

ROWS = [[r + c for c in COL_DIGITS] for r in ROW_LETTERS]
COLS = [[r + c for r in ROW_LETTERS] for c in COL_DIGITS]
TERRITORIES = [cross(rows, cols) for rows in ROW_LETTERS_IN_THREE for cols in COL_DIGITS_IN_THREE]
TOP_DIAGONAL = [r + c for r, c in zip(ROW_LETTERS, COL_DIGITS)]
BOTTOM_DIAGONAL = [r + c for r, c in zip(ROW_LETTERS, list(reversed(COL_DIGITS)))]
DIAGONALS = [TOP_DIAGONAL, BOTTOM_DIAGONAL]
UNIT_LIST = ROWS + COLS + TERRITORIES + DIAGONALS

def in_same_territory(s1, s2):
    return any(territory for territory in TERRITORIES if s1 in territory and s2 in territory)

def peers(square):
    """
    Find all peers for a given square.
    """
    units = [unit for unit in UNIT_LIST if square in unit]
    peers = [peer for unit in units for peer in unit]
    return list(set(filter(lambda s: s != square, peers))) # remove the square itself and duplicates

def only_choice(values):
    for unit in UNIT_LIST:
        for d in DIGITS:
            appearances = [s for s in unit if d in values[s]]
            if len(appearances) == 1:
                assign_value(values, appearances[0], d)
    return values

def is_unsolvable(values):
    return any(len(ds) == 0 for ds in values.values())

def reduce_puzzle(values):
    keep_reducing = True
    while keep_reducing:
        solved_square_count_before = len(solved_squares(values))
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_square_count_after = len(solved_squares(values))
        keep_reducing = solved_square_count_before < solved_square_count_after
    return values

def is_solved(values):
    return len(solved_squares(values)) == 81

def unsolved_square_with_least_possibilities(values):
    _, square = min([(len(ds), s) for s, ds in values.items() if len(ds) > 1])
    return square

def search(values):
    values = reduce_puzzle(values)
    if is_unsolvable(values): return False
    if is_solved(values): return values
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
