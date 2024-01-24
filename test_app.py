import unittest
import json
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_save_data(self):
        data = {"name": "Test User", "age": 30}
        response = self.app.post('/save_data', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'message': 'Data saved successfully'})

    def test_read_data(self):
        response = self.app.get('/read_data')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.get_data(as_text=True)), list)

if __name__ == '__main__':
    unittest.main()
