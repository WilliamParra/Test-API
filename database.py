import psycopg2
from psycopg2 import Error

def create_connection(dbname, user, password, host="localhost", port="5432"):
    """Create a database connection to a PostgreSQL database"""
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=5433
        )
        print("Successfully connected to PostgreSQL database!")
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None
'''
def create_table(connection):
    """Create a sample table in the PostgreSQL database"""
    create_table_query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    
    try:
        # Create a cursor object to execute PostgreSQL commands
        cursor = connection.cursor()
        
        # Execute the table creation command
        cursor.execute(create_table_query)
        
        # Commit the changes
        connection.commit()
        print("Table created successfully!")
        
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()
'''

def main():
    # Database connection parameters
    db_params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "admin1",
        "host": "localhost",  # Change if your database is hosted elsewhere
        "port": "5433"       # Default PostgreSQL port
    }
    
    # Create a connection
    connection = create_connection(**db_params)
    
    if connection:
        
        try:
            # Create a cursor object
            cursor = connection.cursor()
            
            # Example of inserting data
            insert_query = """
                INSERT INTO users (name, age) 
                VALUES (%s, %s) 
                RETURNING id;"""
            cursor.execute(insert_query, ("John Doe", "53"))
            
            # Commit the transaction
            connection.commit()
            
        except Error as e:
            print(f"Error executing query: {e}")
            connection.rollback()
        
        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                print("Database connection closed.")

if __name__ == '__main__':
    main()
