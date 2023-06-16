import sqlite3

class Transaction:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.createTable()

    def createTable(self): #create a table if it does not exist 
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions 
        (item TEXT, 
        amount REAL, 
        category TEXT, 
        date TEXT, 
        description TEXT)''')
        self.conn.commit()

    def addTransaction(self, item, amount, category, date, description): #used in tracker.py to add a transactions
        self.cursor = self.conn.cursor()
        self.cursor.execute('''INSERT INTO transactions
                     (item, amount, category, date, description)
                     VALUES (?, ?, ?, ?, ?)''',
                  (item, amount, category, date, description))
        self.conn.commit()

    def viewTransactions(self): #used in tracker.py to view all transactions
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT * FROM transactions''')
        return self.cursor.fetchall()
    
    def sortByCategory(self, category): #used in tracker.py to sort by category
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT * FROM transactions WHERE category=?''', (category,))
        return self.cursor.fetchall()
    
    def sortByDate(self, date): #used in tracker.py to sort by date
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT * FROM transactions WHERE date=?''', (date,))
        return self.cursor.fetchall()
    
    def sortByAmount(self, amount): #used in tracker.py to sort by amount
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT * FROM transactions WHERE amount=?''', (amount,))
        return self.cursor.fetchall()
    
    def __del__(self): #close connection
        self.conn.close()