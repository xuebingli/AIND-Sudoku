import solution
from solution import DIGITS
import unittest

class TestDiagonalSudoku(unittest.TestCase):
    grid = '.5.......6.3..24...7.1....38.4.....7.........3.....2.97....1.2...96..7.1.......4.'
    values = {
        'A1': DIGITS, 'A2': '5',    'A3': DIGITS, 'A4': DIGITS, 'A5': DIGITS, 'A6': DIGITS, 'A7': DIGITS, 'A8': DIGITS, 'A9': DIGITS,
        'B1': '6',    'B2': DIGITS, 'B3': '3',    'B4': DIGITS, 'B5': DIGITS, 'B6': '2',    'B7': '4',    'B8': DIGITS, 'B9': DIGITS,
        'C1': DIGITS, 'C2': '7',    'C3': DIGITS, 'C4': '1',    'C5': DIGITS, 'C6': DIGITS, 'C7': DIGITS, 'C8': DIGITS, 'C9': '3',
        'D1': '8',    'D2': DIGITS, 'D3': '4',    'D4': DIGITS, 'D5': DIGITS, 'D6': DIGITS, 'D7': DIGITS, 'D8': DIGITS, 'D9': '7',
        'E1': DIGITS, 'E2': DIGITS, 'E3': DIGITS, 'E4': DIGITS, 'E5': DIGITS, 'E6': DIGITS, 'E7': DIGITS, 'E8': DIGITS, 'E9': DIGITS,
        'F1': '3',    'F2': DIGITS, 'F3': DIGITS, 'F4': DIGITS, 'F5': DIGITS, 'F6': DIGITS, 'F7': '2',    'F8': DIGITS, 'F9': '9',
        'G1': '7',    'G2': DIGITS, 'G3': DIGITS, 'G4': DIGITS, 'G5': DIGITS, 'G6': '1',    'G7': DIGITS, 'G8': '2',    'G9': DIGITS,
        'H1': DIGITS, 'H2': DIGITS, 'H3': '9',    'H4': '6',    'H5': DIGITS, 'H6': DIGITS, 'H7': '7',    'H8': DIGITS, 'H9': '1',
        'I1': DIGITS, 'I2': DIGITS, 'I3': DIGITS, 'I4': DIGITS, 'I5': DIGITS, 'I6': DIGITS, 'I7': DIGITS, 'I8': '4',    'I9': DIGITS
    }

    def test_grid_values(self):
        self.assertEqual(solution.grid_values(self.grid), self.values)

    def test_cross(self):
        rows = 'ABC'
        digits = '12'
        self.assertEqual(solution.cross(rows, digits), ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])

    def test_in_three(self):
        self.assertEqual(solution.in_three('ABCDEFGHI'), ['ABC', 'DEF', 'GHI'])

    def test_in_same_territory(self):
        self.assertTrue(solution.in_same_territory('E2', 'D1'))
        self.assertFalse(solution.in_same_territory('E2', 'A1'))

    def test_is_unsolvable(self):
        unsolvable_values = self.values.copy()
        unsolvable_values['A1'] = ''
        self.assertTrue(solution.is_unsolvable(unsolvable_values))

    def test_eliminate(self):
        eliminated_values = solution.eliminate(self.values.copy())
        self.assertEqual(eliminated_values['E2'], '1269')
        self.assertEqual(eliminated_values['A1'], '1249')

    def test_only_choice(self):
        eliminated_values = solution.eliminate(self.values.copy())
        processed_values = solution.only_choice(eliminated_values)
        self.assertEqual(processed_values, {
            'A1': '1249', 'A2': '5', 'A3': '128', 'A4': '34789', 'A5': '346789', 'A6': '346789', 'A7': '1689', 'A8': '16789', 'A9': '2',
            'B1': '6', 'B2': '189', 'B3': '3', 'B4': '5789', 'B5': '5789', 'B6': '2', 'B7': '4', 'B8': '15789', 'B9': '58',
            'C1': '249', 'C2': '7', 'C3': '28', 'C4': '1', 'C5': '45689', 'C6': '45689', 'C7': '5689', 'C8': '5689', 'C9': '3',
            'D1': '8', 'D2': '1269', 'D3': '4', 'D4': '2359', 'D5': '123569', 'D6': '3569', 'D7': '1356', 'D8': '1356', 'D9': '7',
            'E1': '1259', 'E2': '1269', 'E3': '12567', 'E4': '2345789', 'E5': '123456789', 'E6': '3456789', 'E7': '13568', 'E8': '13568', 'E9': '4',
            'F1': '3', 'F2': '16', 'F3': '1567', 'F4': '4578', 'F5': '145678', 'F6': '45678', 'F7': '2', 'F8': '1568', 'F9': '9',
            'G1': '7', 'G2': '3468', 'G3': '568', 'G4': '34589', 'G5': '34589', 'G6': '1', 'G7': '35689', 'G8': '2', 'G9': '568',
            'H1': '245', 'H2': '2348', 'H3': '9', 'H4': '6', 'H5': '23458', 'H6': '3458', 'H7': '7', 'H8': '358', 'H9': '1',
            'I1': '125', 'I2': '12368', 'I3': '12568', 'I4': '235789', 'I5': '235789', 'I6': '35789', 'I7': '35689', 'I8': '4', 'I9': '568'
        })

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
