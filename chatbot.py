import mysql.connector
import datetime
import time
from mysql.connector import Error

def setup_db():
    """Initialize the MySQL database and create the chats table if not exists."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Neobot',  # Change this to your database name
            user='root',  # Change to your MySQL username
            password='kapil'  # Change to your MySQL password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(255),
                    message TEXT,
                    timestamp DATETIME
                )
            ''')
            connection.commit()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def add_message(user_id, message):
    """Add a message to the database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Neobot',
            user='root',
            password='kapil'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("INSERT INTO chats (user_id, message, timestamp) VALUES (%s, %s, %s)",
                           (user_id, message, datetime.datetime.now()))
            connection.commit()
    except Error as e:
        print(f"Error adding message: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def clean_old_messages(hours=24):
    """Delete messages older than the specified number of hours."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Neobot',
            user='root',
            password='kapil'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cutoff = datetime.datetime.now() - datetime.timedelta(hours=hours)
            cursor.execute("DELETE FROM chats WHERE timestamp < %s", (cutoff,))
            connection.commit()
    except Error as e:
        print(f"Error cleaning old messages: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    """Main function to run the chatbot simulation."""
    setup_db()
    
    # Simulate receiving messages
    for i in range(10):
        add_message(user_id=f"User_{i}", message=f"Message number {i}")
        print(f"Added message: User_{i} - Message number {i}")
        time.sleep(1)  # Simulate time between messages

    # Clean old messages every hour for demonstration
    while True:
        clean_old_messages()
        print("Cleaned old messages.")
        time.sleep(3600)  # Check every hour, but for testing, you might want to use a much shorter interval

if __name__ == "__main__":
    main()