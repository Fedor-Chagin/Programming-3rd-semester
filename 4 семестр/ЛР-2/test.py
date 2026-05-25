import unittest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from task import ConcreteComponent, ToYAMLDecorator, ToCSVDecorator


class TestDecorators(unittest.TestCase):
    
    def setUp(self):
        self.component = ConcreteComponent(['USD'])
    
    @patch('urllib.request.urlopen')
    def test_concrete_component_returns_dict(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = self.component.operation()
        self.assertIsInstance(result, dict)
        self.assertIn('rates', result)
    
    @patch('urllib.request.urlopen')
    def test_concrete_component_has_usd(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = self.component.operation()
        self.assertIn('USD', result['rates'])
    
    @patch('urllib.request.urlopen')
    def test_network_error_returns_zeros(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("No internet")
        
        result = self.component.operation()
        self.assertEqual(result['date'], '0000-00-00')
        self.assertEqual(result['rates']['USD'], 0)
        self.assertIn('error', result)
    
    @patch('urllib.request.urlopen')
    def test_yaml_decorator_returns_str(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToYAMLDecorator(self.component)
        result = decorator.operation()
        self.assertIsInstance(result, str)
        self.assertIn('USD', result)
    
    @patch('urllib.request.urlopen')
    def test_yaml_decorator_saves_file(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToYAMLDecorator(self.component)
        
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as tmp:
            filename = tmp.name
        
        try:
            saved_file = decorator.save_to_file(filename)
            self.assertTrue(os.path.exists(saved_file))
            with open(saved_file, 'r') as f:
                content = f.read()
                self.assertIn('USD', content)
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    @patch('urllib.request.urlopen')
    def test_csv_decorator_returns_str(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToCSVDecorator(self.component)
        result = decorator.operation()
        self.assertIsInstance(result, str)
        self.assertIn('USD', result)
    
    @patch('urllib.request.urlopen')
    def test_csv_decorator_has_csv_format(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToCSVDecorator(self.component)
        result = decorator.operation()
        self.assertIn('date,currency,rate', result)
    
    @patch('urllib.request.urlopen')
    def test_csv_decorator_saves_file(self, mock_urlopen):
        mock_data = {
            'Date': '2024-01-15T00:00:00',
            'Valute': {'USD': {'Value': 75.5}}
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        decorator = ToCSVDecorator(self.component)
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            filename = tmp.name
        
        try:
            saved_file = decorator.save_to_file(filename)
            self.assertTrue(os.path.exists(saved_file))
        finally:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == '__main__':
    unittest.main()