import pytest
import sqlite3
from transaction import Transaction

@pytest.fixture
def tracker():
    return Transaction(':memory:')

def test_create_table(tracker):
    tracker.create_table()
    tracker.cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';''')
    result = tracker.cursor.fetchone()
    assert result is not None

def test_add_transaction(tracker):
    tracker.add_transaction('car', 10.0, 'vechile', '2022-01-20', 'Big and red')
    tracker.cursor.execute('''SELECT COUNT(*) FROM transactions WHERE item='car';''')
    result = tracker.cursor.fetchone()[0]
    assert result == 1

def test_view_transactions(tracker):
    tracker.add_transaction('bike', 5.0, 'vechile', '2021-02-25', 'blue')
    tracker.add_transaction('strawberry', 20.0, 'fruit', '2020-05-11', 'red')
    result = tracker.view_transactions()
    assert len(result) == 2

def test_view_transactions_by_category(tracker):
    tracker.add_transaction('car', 10.0, 'vechile', '2022-01-20', 'Big and red')
    tracker.add_transaction('bike', 5.0, 'vechile', '2021-02-25', 'blue')
    result = tracker.view_transactions_by_category('vechile')
    assert len(result) == 2

def test_view_transactions_by_date(tracker):
    tracker.add_transaction('fish', 30.0, 'animal', '2022-01-01', 'long and thin')
    tracker.add_transaction('Tree', 11.0, 'plant', '1988-05-03', 'tall and green')
    result = tracker.view_transactions_by_date('2022-01-01')
    assert len(result) == 1

def test_view_transactions_by_amount(tracker):
    tracker.add_transaction('Sppon', 11.0, 'utencil', '2018-01-01', 'Silver')
    tracker.add_transaction('Yak-141', 11.0, 'aircraft', '1987-03-09', 'VTOL')
    tracker.add_transaction('Tree', 11.0, 'plant', '1988-05-03', 'tall and green')
    result = tracker.view_transactions_by_amount(11.0)
    assert len(result) == 3
