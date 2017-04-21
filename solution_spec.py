import solution
from solution import DIGITS
import unittest

class TestStandardSudoku(unittest.TestCase):
    grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    values = {
        'A1': DIGITS, 'A2': DIGITS, 'A3': '3', 'A4': DIGITS, 'A5': '2', 'A6': DIGITS, 'A7': '6', 'A8': DIGITS, 'A9': DIGITS,
        'B1': '9', 'B2': DIGITS, 'B3': DIGITS, 'B4': '3', 'B5': DIGITS, 'B6': '5', 'B7': DIGITS, 'B8': DIGITS, 'B9': '1',
        'C1': DIGITS, 'C2': DIGITS, 'C3': '1', 'C4': '8', 'C5': DIGITS, 'C6': '6', 'C7': '4', 'C8': DIGITS, 'C9': DIGITS,
        'D1': DIGITS, 'D2': DIGITS, 'D3': '8', 'D4': '1', 'D5': DIGITS, 'D6': '2', 'D7': '9', 'D8': DIGITS, 'D9': DIGITS,
        'E1': '7', 'E2': DIGITS, 'E3': DIGITS, 'E4': DIGITS, 'E5': DIGITS, 'E6': DIGITS, 'E7': DIGITS, 'E8': DIGITS, 'E9': '8',
        'F1': DIGITS, 'F2': DIGITS, 'F3': '6', 'F4': '7', 'F5': DIGITS, 'F6': '8', 'F7': '2', 'F8': DIGITS, 'F9': DIGITS,
        'G1': DIGITS, 'G2': DIGITS, 'G3': '2', 'G4': '6', 'G5': DIGITS, 'G6': '9', 'G7': '5', 'G8': DIGITS, 'G9': DIGITS,
        'H1': '8', 'H2': DIGITS, 'H3': DIGITS, 'H4': '2', 'H5': DIGITS, 'H6': '3', 'H7': DIGITS, 'H8': DIGITS, 'H9': '9',
        'I1': DIGITS, 'I2': DIGITS, 'I3': '5', 'I4': DIGITS, 'I5': '1', 'I6': DIGITS, 'I7': '3', 'I8': DIGITS, 'I9': DIGITS
    }

    def test_cross(self):
        rows = 'ABC'
        digits = '12'
        self.assertEqual(solution.cross(rows, digits), ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])

    def test_grid_values(self):
        self.assertEqual(solution.grid_values(self.grid), self.values)

    def test_in_three(self):
        self.assertEqual(solution.in_three('ABCDEFGHI'), ['ABC', 'DEF', 'GHI'])

    def test_territory_of_square(self):
        self.assertEqual(solution.territory_of_square('E2'), ['D1', 'D2', 'D3',
                                                         'E1', 'E2', 'E3',
                                                         'F1', 'F2', 'F3'])
        self.assertEqual(solution.territory_of_square('I9'), ['G7', 'G8', 'G9',
                                                         'H7', 'H8', 'H9',
                                                         'I7', 'I8', 'I9'])

    def test_only_choice(self):
        eliminated_values = self.values.copy()
        eliminated_values['A4'] = '49'
        eliminated_values['A6'] = '147'
        eliminated_values['B5'] = '47'
        eliminated_values['C5'] = '79'
        processed_values = solution.only_choice(eliminated_values)
        self.assertEqual(processed_values['A6'], '1')

class TestDiagonalSudoku(unittest.TestCase):
    values = {
        'A1': DIGITS, 'A2': '5', 'A3': DIGITS, 'A4': DIGITS, 'A5': DIGITS, 'A6': DIGITS, 'A7': DIGITS, 'A8': DIGITS, 'A9': DIGITS,
        'B1': '6', 'B2': DIGITS, 'B3': '3', 'B4': DIGITS, 'B5': DIGITS, 'B6': '2', 'B7': '4', 'B8': DIGITS, 'B9': DIGITS,
        'C1': DIGITS, 'C2': '7', 'C3': DIGITS, 'C4': '1', 'C5': DIGITS, 'C6': DIGITS, 'C7': DIGITS, 'C8': DIGITS, 'C9': '3',
        'D1': '8', 'D2': DIGITS, 'D3': '4', 'D4': DIGITS, 'D5': DIGITS, 'D6': DIGITS, 'D7': DIGITS, 'D8': DIGITS, 'D9': '7',
        'E1': DIGITS, 'E2': DIGITS, 'E3': DIGITS, 'E4': DIGITS, 'E5': DIGITS, 'E6': DIGITS, 'E7': DIGITS, 'E8': DIGITS, 'E9': DIGITS,
        'F1': '3', 'F2': DIGITS, 'F3': DIGITS, 'F4': DIGITS, 'F5': DIGITS, 'F6': DIGITS, 'F7': '2', 'F8': DIGITS, 'F9': '9',
        'G1': '7', 'G2': DIGITS, 'G3': DIGITS, 'G4': DIGITS, 'G5': DIGITS, 'G6': '1', 'G7': DIGITS, 'G8': '2', 'G9': DIGITS,
        'H1': DIGITS, 'H2': DIGITS, 'H3': '9', 'H4': '6', 'H5': DIGITS, 'H6': DIGITS, 'H7': '7', 'H8': DIGITS, 'H9': '1',
        'I1': DIGITS, 'I2': DIGITS, 'I3': DIGITS, 'I4': DIGITS, 'I5': DIGITS, 'I6': DIGITS, 'I7': DIGITS, 'I8': '4', 'I9': DIGITS
    }

    def test_eliminate(self):
        eliminated_values = solution.eliminate(self.values)
        self.assertEqual(eliminated_values['E2'], '1269')
        self.assertEqual(eliminated_values['A1'], '1249')

    def test_peers(self):
        self.assertCountEqual(solution.peers('E2'), set(['E1', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
                                                         'A2', 'B2', 'C2', 'D2', 'F2', 'G2', 'H2', 'I2',
                                                         'D1', 'D2', 'D3', 'E1', 'E3', 'F1', 'F2', 'F3']))
        self.assertCountEqual(solution.peers('A1'), set(['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                                                         'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1',
                                                         'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3',
                                                         'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']))

if __name__ == '__main__':
    unittest.main()
