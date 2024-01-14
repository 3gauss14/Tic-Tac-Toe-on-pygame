import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('tic_tac_toe.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                winner TEXT,
                game_type TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def insert_statistics(self, winner, game_type):
        self.cursor.execute('''
            INSERT INTO statistics (winner, game_type) VALUES (?, ?)
        ''', (winner, game_type))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
