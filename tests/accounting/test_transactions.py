import pytest
from tfin.accounting import Transaction, TransactionItem, UnbalancedTransactionError

@pytest.fixture
def transaction():
    return Transaction(timestep=2, name="Test Transaction")


@pytest.fixture
def filled_transaction(transaction, asset, expense):
    asset.set_balance(100)

    transaction.add_credit(TransactionItem(asset, 20))
    transaction.add_debit(TransactionItem(expense, 20))

    return transaction


def test_transaction(filled_transaction):
    """Test creation and inspection of a transaction"""

    assert filled_transaction.total_debits == 20, "Debit not added correctly"
    assert filled_transaction.total_credits == 20, "Credit not added correctly"
    assert filled_transaction.n_entries == 2, "N_entries not correct"
    assert filled_transaction.is_balanced, "Balanced transaction shown as unbalanced"

    asset = filled_transaction.credits[0].account
    expense = filled_transaction.debits[0].account

    for _ in filled_transaction():
        pass

    assert expense.balance == 20, "Expense balance should be 20"
    assert asset.balance == 80


def test_unbalanced_transaction(transaction, asset):
    """Ensure an unbalanced transaction does not execute"""
    transaction.add_credit(asset, 100)

    assert not transaction.is_balanced

    with pytest.raises(UnbalancedTransactionError):
        for _ in transaction():
            pass

    assert asset.balance == 0


def test_transaction_by_account(transaction, asset, expense):
    """Test adding a transaction by account and amount rather that a dedicated TransactionItem"""

    transaction.add_debit(asset, 50)
    transaction.add_credit(expense, 50)

    assert transaction.n_entries == 2
    assert transaction.is_balanced


def test_bad_transaction(transaction, asset):
    """Tests bad formation of transactions"""

    asset.set_balance(100)

    transaction.add_credit(25.0)
    transaction.add_debit("34")
    assert transaction.n_entries == 0

    transaction.add_credit(TransactionItem(asset, 55))

    with pytest.raises(UnbalancedTransactionError):
        transaction()

    assert asset.balance == 100

    transaction.clear()
    transaction.add_debit(asset)
    transaction.add_credit(asset)

    assert transaction.n_entries == 0
