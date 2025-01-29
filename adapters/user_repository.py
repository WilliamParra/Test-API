from decorators import db_connection


class UserRepository:

    @db_connection
    def insert_user(self, cursor, connection, name, age):
        cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
        connection.commit()

    @db_connection
    def fetch_all_users(self, cursor, connection):
        cursor.execute("SELECT id, name, age FROM users;")
        users = cursor.fetchall()
        return [{"id": u[0], "name": u[1], "age": u[2]} for u in users]

    @db_connection
    def search_by_name(self, cursor, connection, name):
        cursor.execute(
            """
            SELECT id, name, age 
            FROM users 
            WHERE LOWER(SPLIT_PART(name, ' ', 1)) = LOWER(%s);
            """,
            (name,),
        )
        users = cursor.fetchall()
        return [{"id": u[0], "name": u[1], "age": u[2]} for u in users]
