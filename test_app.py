import unittest
import json
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Define data IDs for testing
        self.data_ids = [1, 2, 3]  # Add more data IDs as needed

    def test_create_data(self):
        data = {"value1": "Test Value 1", "value2": "Test Value 2"}
        response = self.app.post('/create_data', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'message': 'Data created successfully'})

    def test_read_all_data(self):
        response = self.app.get('/read_all_data')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.get_data(as_text=True)), list)

    def test_read_data(self):
        for data_id in self.data_ids:
            response = self.app.get(f'/read_data/{data_id}')
            self.assertEqual(response.status_code, 200)
            # Adjust the expected JSON structure based on your application logic
            self.assertIsInstance(json.loads(response.get_data(as_text=True)), dict)

    def test_update_data(self):
        data = {"value1": "Updated Value 1", "value2": "Updated Value 2"}
        for data_id in self.data_ids:
            response = self.app.put(f'/update_data/{data_id}', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.get_data(as_text=True)), {'message': 'Data updated successfully'})

    def test_delete_data(self):
        for data_id in self.data_ids:
            response = self.app.delete(f'/delete_data/{data_id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.get_data(as_text=True)), {'message': 'Data deleted successfully'})

if __name__ == '__main__':
    unittest.main()
