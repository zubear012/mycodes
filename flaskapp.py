from flask import Flask, request, jsonify
from db_queries import insert_data, get_all_data, update_data, delete_data
app = Flask(__name__)
# Switcher function to handle different HTTP methods
def switcher(request_method, user_id=None):
    if request_method == 'POST':
        data = request.get_json()
        user_id = data['user_id']
        name = data['name']
        age = data['age']
        insert_data(user_id, name, age)
        return jsonify({'message': 'Data inserted successfully'}), 201

    elif request_method == 'GET':
        if user_id is None:
            data_list = get_all_data()
            return jsonify(data_list)
        else:
            # Handle specific GET request if needed
            pass

    elif request_method == 'PUT':
        data = request.get_json()
        new_name = data.get('name')
        new_age = data.get('age')
        update_data(user_id, new_name, new_age)
        return jsonify({'message': 'Data updated successfully'}), 200

    elif request_method == 'DELETE':
        delete_data(user_id)
        return jsonify({'message': 'Data deleted successfully'}), 200

    else:
        return jsonify({'error': 'Invalid request method'}), 400

# Route to handle requests
@app.route('/api/data', methods=['POST', 'GET'])
@app.route('/api/data/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_requests(user_id=None):
    request_method = request.method
    return switcher(request_method, user_id)

if __name__ == '__main__':
    app.run(debug=True)

