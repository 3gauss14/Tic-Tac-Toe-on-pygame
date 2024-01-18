import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("data/stats.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_type TEXT,
                player_1_wins INTEGER,
                player_2_wins INTEGER,
                computer_wins INTEGER
            )
        """)
        self.connection.commit()

    def update_stats(self, game_type, player_1_wins=0, player_2_wins=0, computer_wins=0):
        self.cursor.execute("""
            INSERT INTO stats (game_type, player_1_wins, player_2_wins, computer_wins)
            VALUES (?, ?, ?, ?)
        """, (game_type, player_1_wins, player_2_wins, computer_wins))
        self.connection.commit()
