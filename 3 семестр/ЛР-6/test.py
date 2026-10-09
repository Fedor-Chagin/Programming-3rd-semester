import unittest
from unittest.mock import patch, Mock
from io import StringIO
import sys

from task import get_currencies_v1, get_currencies_v2, get_currencies

class TestTaskSimple(unittest.TestCase):
    
    def test_all_versions_return_dict(self):
        for func in [get_currencies_v1, get_currencies_v2, get_currencies]:
            result = func(['USD', 'EUR'])
            self.assertIsInstance(result, dict)
            self.assertIn('USD', result)
            self.assertIn('EUR', result)
    
    def test_all_versions_return_none_on_error(self):
        for func in [get_currencies_v1, get_currencies_v2, get_currencies]:
            result = func(['XXX'])
            self.assertIsNone(result)
    
    def test_v1_prints_error(self):
        captured = StringIO()
        sys.stdout = captured
        get_currencies_v1(['XXX'])
        sys.stdout = sys.__stdout__
        self.assertIn('XXX', captured.getvalue())
    
    def test_v2_prints_error(self):
        captured = StringIO()
        sys.stdout = captured
        get_currencies_v2(['XXX'])
        sys.stdout = sys.__stdout__
        self.assertIn('XXX', captured.getvalue())
    
    def test_mocked_api_error(self):
        mock_response = Mock()
        mock_response.json.return_value = {"foo": "bar"}
        mock_response.raise_for_status = Mock()
        
        with patch('task.requests.get', return_value=mock_response):
            for func in [get_currencies_v1, get_currencies_v2, get_currencies]:
                result = func(['USD'])
                self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()