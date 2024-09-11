import sqlite3

class Memory:
    def __init__(self):
        self.conn = sqlite3.connect('memory.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS interactions
                         (id INTEGER PRIMARY KEY, user_input TEXT, ai_response TEXT)''')

    def store_interaction(self, user_input, ai_response):
        self.c.execute("INSERT INTO interactions (user_input, ai_response) VALUES (?, ?)",
                       (user_input, ai_response))
        self.conn.commit()

    def get_last_interaction(self):
        self.c.execute("SELECT * FROM interactions ORDER BY id DESC LIMIT 1")
        return self.c.fetchone()
