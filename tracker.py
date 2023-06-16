from transaction import Transaction

tracker = Transaction('tracker.db')

def showCategories(tracker):
    categories = set([row[2] for row in tracker.viewTransactions()])
    if categories:
        print('Categories:')
        for category in categories:
            print(f'- {category}')
    else:
        print('No categories found.')

def addCategory(tracker):
    category = input('Enter a new category name: ')
    tracker.addTransaction(None, None, category, None, None)
    print(f'Added category {category}.')
    
def modifyCategory(tracker):
    old_category = input('Enter the name of the category to modify: ')
    new_category = input('Enter the new name for the category: ')
    cursor = tracker.conn.cursor()
    cursor.execute('UPDATE transactions SET category = ? WHERE category = ?', 
                   (new_category, old_category))
    tracker.conn.commit()
    print(f'Modified {cursor.rowcount} transactions from {old_category} to {new_category}.')

def showTransactions(tracker):
    transactions = tracker.viewTransactions()
    if transactions:
        print('Transactions:')
        for transaction in transactions:
            print(f'- {transaction[1]}: ${transaction[2]:.2f} ({transaction[3]}, {transaction[4]}, {transaction[5]})')
    else:
        print('No transactions found.')

def addTransaction(tracker):
    item = input('Enter the item: ')
    amount = float(input('Enter the amount: '))
    category = input('Enter the category: ')
    date = input('Enter the date (YYY-MM-DD): ')
    description = input('Enter a description: ')
    tracker.addTransaction(item, amount, category, date, description)
    print('Added transaction.')

def deleteTransaction(tracker):
    item = input('Enter the item of the transaction to delete: ')
    cursor = tracker.conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE item_number = ?', (item,))
    tracker.conn.commit()
    print(f'Deleted {cursor.rowcount} transactions.')

def sortDate(tracker):
    cursor = tracker.conn.cursor()
    cursor.execute('SELECT date, SUM(amount) FROM transactions GROUP BY date')
    rows = cursor.fetchall()
    if rows:
        print('Transactions by date:')
        for row in rows:
            print(f'- {row[0]}: ${row[1]:.2f}')
    else:
        print('No transactions found.')

def sortMonth(tracker):
    cursor = tracker.conn.cursor()
    cursor.execute('SELECT strftime("%Y-%m", date) as month, SUM(amount) FROM transactions GROUP BY month')
    rows = cursor.fetchall()
    if rows:
        print('Transactions by month:')
        for row in rows:
            print(f'- {row[0]}: ${row[1]:.2f}')
    else:
        print('No transactions found.')

def sortYear(tracker):
    cursor = tracker.conn.cursor()
    cursor.execute('SELECT strftime("%Y", date) as year, SUM(amount) FROM transactions GROUP BY year')
    rows = cursor.fetchall()
    if rows:
        print('Transactions by year:')
        for row in rows:
            print(f'- {row[0]}: ${row[1]:.2f}')
    else:
        print('No transactions found.')

def sortCategory(tracker):
    cursor = tracker.conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM transactions GROUP BY category')
    rows = cursor.fetchall()
    if rows:
        print('Transactions by category:')
        for row in rows:
            print(f'- {row[0]}: ${row[1]:.2f}')
    else:
        print('No transactions found.') 

    