from flask import Flask, jsonify, request
import mysql.connector
import json
from urllib.parse import quote as url_quote
#from configparser import ConfigParser

app = Flask(__name__)

#database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'root',
    'database': 'week1',
}
with open('config.json', 'r') as file:
    config = json.load(file)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.route('/')
def default_port():
    return "This is default"


# Define a route for creating data (POST request)
@app.route('/create_data', methods=['POST'])
def create_data():
    try:
        data = request.json

        # Example: Save data to the database
        query = "INSERT INTO table1 (value1, value2) VALUES (%s, %s)"
        values = (data['value1'], data['value2'])
        cursor.execute(query, values)
        conn.commit()

        return jsonify({'message': 'Data created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define a route for reading all data (GET request)
@app.route('/read_all_data', methods=['GET'])
def read_all_data():
    try:
        # Example: Read all data from the database
        query = "SELECT * FROM table1"
        cursor.execute(query)
        result = cursor.fetchall()

        # Convert result to a list of dictionaries for JSON response
        data_list = [{'value1': row[1], 'value2': row[2]} for row in result]

        return jsonify(data_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define a route for reading specific data by ID (GET request)
@app.route('/read_data/<int:data_id>', methods=['GET'])
def read_data(data_id):
    try:
        # Example: Read specific data from the database by ID
        query = "SELECT * FROM table1 WHERE id = %s"
        cursor.execute(query, (data_id,))
        result = cursor.fetchone()

        if result:
            data_dict = {'value1': result[1], 'value2': result[2]}
            return jsonify(data_dict)
        else:
            return jsonify({'message': 'Data not found'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define a route for updating data by ID (PUT request)
@app.route('/update_data/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    try:
        data = request.json

        # Example: Update data in the database by ID
        query = "UPDATE table1 SET value1 = %s, value2 = %s WHERE id = %s"
        values = (data['value1'], data['value2'], data_id)
        cursor.execute(query, values)
        conn.commit()

        return jsonify({'message': 'Data updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define a route for deleting data by ID (DELETE request)
@app.route('/delete_data/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    try:
        # Example: Delete data from the database by ID
        query = "DELETE FROM table1 WHERE id = %s"
        cursor.execute(query, (data_id,))
        conn.commit()

        return jsonify({'message': 'Data deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
