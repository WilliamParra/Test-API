from models import User


class UserRepository:
    def __init__(self, cursor):
        self.cursor = cursor

    def create(self, name, age):
        self.cursor.excecute(
            "INSERT INTO users (name, age) VALUES (%s, %s)", (name, age)
        )

    def get_all(self):
        self.cursor.execute("SELECT id, name, age FROM users")
        rows = self.cursor.fetchall()
        return [User.from_db_row(row) for row in rows]

    def search_by_name(self, name):
        self.cursor.execute(
            """
                SELECT id, name, age 
                FROM users
                WHERE LOWER(SPLIT_PART(name,' ',1)) = LOWER(%s)
            """,
            (name,),
        )
        rows = self.cursor.fetchall()
        return [User.from_db_row(row) for row in rows]

    def get_by_id(self, id):
        self.cursor.execute(
            """
                SELECT id, name, age
                FROM users
                WHERE id = %s
            """,
            (id,),
        )
        row = self.cursor.fetchone()
        return User.from_db_row(row) if row else None
