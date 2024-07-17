import unittest
from datetime import datetime, timedelta
from collections import defaultdict
from data_extractor import calculate_time_and_days, calculate_longest_session


class TestScript(unittest.TestCase):

    def setUp(self):
        # Mock data to be used in tests
        self.mock_data = defaultdict(list, {
            'user1': [('GATE_IN', datetime(2023, 2, 1, 9, 0, 0)), ('GATE_OUT', datetime(2023, 2, 1, 17, 0, 0))],
            'user2': [('GATE_IN', datetime(2023, 2, 1, 8, 0, 0)), ('GATE_OUT', datetime(2023, 2, 1, 16, 0, 0)),
                      ('GATE_IN', datetime(2023, 2, 2, 9, 0, 0)), ('GATE_OUT', datetime(2023, 2, 2, 17, 0, 0))]
        })

    def test_calculate_time_and_days(self):
        result = calculate_time_and_days(self.mock_data)
        expected_result = [
            ('user1', 8.0, 1, 8.0, 1),  # user_id, total_hours, num_days, avg_per_day, rank
            ('user2', 16.0, 2, 8.0, 2)
        ]
        self.assertEqual(result, expected_result)

    def test_calculate_longest_session(self):
        # Changing the mock data to match IN/OUT events
        self.mock_data = defaultdict(list, {
            'user1': [('GATE_IN', datetime(2023, 2, 1, 9, 0, 0)), ('GATE_OUT', datetime(2023, 2, 1, 19, 0, 0))],
            'user2': [('GATE_IN', datetime(2023, 2, 1, 8, 0, 0)), ('GATE_OUT', datetime(2023, 2, 1, 16, 0, 0)),
                      ('GATE_IN', datetime(2023, 2, 2, 9, 0, 0)), ('GATE_OUT', datetime(2023, 2, 2, 17, 0, 0))]
        })
        result = calculate_longest_session(self.mock_data)
        expected_result = [('user1', 10.0)]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
