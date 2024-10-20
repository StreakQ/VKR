

if __name__ == "__main__":
    database = DatabaseFactory.create_database('sqlite', 'example.db')
    database.connect()

    # Пример запроса
    cursor = database.execute_query('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    database.conn.commit()

    cursor = database.execute_query('SELECT * FROM users')
    result = database.fetch_all(cursor)

    print(result)
    database.disconnect()