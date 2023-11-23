from db_connection import get_db_connection, get_cursor

# Function to insert data into the database
def insert_data(user_id, name, age):
    try:
        connection = get_db_connection()
        cursor = get_cursor(connection)

        insert_query = "INSERT INTO users (user_id, name, age) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, name, age))
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        raise e

# Function to retrieve data from the database
def get_all_data():
    try:
        connection = get_db_connection()
        cursor = get_cursor(connection)

        select_query = "SELECT * FROM users"
        cursor.execute(select_query)

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        data_list = []
        for row in rows:
            data_dict = {
                'id': row[0],
                'name': row[1],
                'age': row[2]
            }
            data_list.append(data_dict)

        return data_list
    except Exception as e:
        raise e

# Function to update data in the database
def update_data(user_id, new_name, new_age):
    try:
        connection = get_db_connection()
        cursor = get_cursor(connection)

        update_query = "UPDATE users SET name = %s, age = %s WHERE user_id = %s"
        cursor.execute(update_query, (new_name, new_age, user_id))
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        raise e

# Function to delete data from the database
def delete_data(user_id):
    try:
        connection = get_db_connection()
        cursor = get_cursor(connection)

        delete_query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(delete_query, (user_id,))
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        raise e
