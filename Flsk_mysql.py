from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Smartbots@1999',
    'database': 'test'
}

# Function to establish a connection to the MySQL database
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Route to handle POST requests for inserting data into the database
@app.route('/api/data', methods=['POST'])
def insert_data():
    try:
        # Get data from the POST request
        data = request.get_json()
        name = data['name']
        age = data['age']
        user_id=data['user_id']

        # Establish a database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert data into the database
        insert_query = "INSERT INTO users (user_id,name, age) VALUES (%s,%s, %s)"
        cursor.execute(insert_query, (user_id,name, age))
        connection.commit()

        # Close the database connection
        cursor.close()
        connection.close()

        # Return success response
        return jsonify({'message': 'Data inserted successfully'}), 201

    except Exception as e:
        # Handle errors and return error response
        return jsonify({'error': str(e)}), 500

# Route to handle GET requests for retrieving data from the database
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Establish a database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve data from the database
        select_query = "SELECT * FROM users"
        cursor.execute(select_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Close the database connection
        cursor.close()
        connection.close()

        # Prepare response data
        data_list = []
        for row in rows:
            data_dict = {
                'id':row[0],
                'name': row[1],
                'age': row[2]
            }
            data_list.append(data_dict)

        # Return data as JSON response
        return jsonify(data_list)

    except Exception as e:
        # Handle errors and return error response
        return jsonify({'error': str(e)}), 500
# Update Data (PUT Request)
@app.route('/api/data/<int:user_id>', methods=['PUT'])
def update_data(user_id):
    try:
        # Get data from the PUT request
        data = request.get_json()
        new_name = data.get('name')
        new_age = data.get('age')

        # Establish a database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Update data in the database
        update_query = "UPDATE users SET name = %s, age = %s WHERE user_id = %s"
        cursor.execute(update_query, (new_name, new_age, user_id))
        connection.commit()    

        # Close the database connection
        cursor.close()
        connection.close()

        # Return success response
        return jsonify({'message': 'Data updated successfully'}), 200

    except Exception as e:
        # Handle errors and return error response
        return jsonify({'error': str(e)}), 500

# Delete Data (DELETE Request)
@app.route('/api/data/<int:user_id>', methods=['DELETE'])
def delete_data(user_id):
    try:
        # Establish a database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Delete data from the database
        delete_query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(delete_query, (user_id,))
        connection.commit()

        # Close the database connection
        cursor.close()
        connection.close()

        # Return success response
        return jsonify({'message': 'Data deleted successfully'}), 200

    except Exception as e:
        # Handle errors and return error response
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)
