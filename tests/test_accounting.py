import pytest
from tfin.accounting import *


@pytest.fixture
def asset():
    return Asset("Test Asset Account")


@pytest.fixture
def liability():
    return Liability("Test Liability Account")


@pytest.fixture
def equity():
    return Equity("Test Equity Account")


@pytest.fixture
def income():
    return Income("Test Income Account")


@pytest.fixture
def expense():
    return Expense("Test Expense Account")


@pytest.fixture
def coa():
    return ChartOfAccounts()


@pytest.fixture
def transaction():
    return Transaction(timestamp=2, name="Test Transaction")


@pytest.fixture
def filled_transaction(transaction, asset, expense):
    asset.set_balance(100)

    transaction.add_credit(TransactionItem(asset, 20))
    transaction.add_debit(TransactionItem(expense, 20))

    return transaction


def test_account_string(asset):
    """Checks the account string is represented"""

    asset.set_balance(120)
    assert "$120.00" in str(asset), str(asset)


def test_account_types():
    """Checks the Account typing design"""
    cash_acct = Asset(name="Cash")

    assert isinstance(cash_acct, Account), "cash_acct not instance Type[Account]"
    assert issubclass(Asset, Account), "Asset class not a subclassof Account"


def test_accounts_mapping():
    """Checks the account mapping exists and returns appropriate results"""
    assert accounts_by_type, "Empty accounts mapping"
    assert accounts_by_type[AccountType.INCOME] == Income, "Check the accounts mapping"


def test_debit_credit(asset, expense, income):
    """Test that the debit/credit methods work in line with accounting terminology"""
    asset.set_balance(100)

    # Paying a bill, you debit the expense, credit the asset
    # The balance should go down
    asset.credit(20)
    expense.debit(20)

    assert asset.balance == 80, "AssetLike mixin incorrect - asset"
    assert expense.balance == 20, "AssetLike mixin incorrect - expense"

    # Making a sale, debit the asset, credit the income
    #  Asset increases, Income increases
    asset.debit(25)
    income.credit(25)

    assert asset.balance == 105
    assert income.balance == 25


def test_coa_account_management(coa, asset):
    """Test the account management handling of the COA"""
    assert len(coa) == 0, "Non empty accounts initialized in COA"
    assert not coa.has_account(asset), "has_account method incorrectly returning"

    coa.add_account(asset)
    assert len(coa) == 1, "Account not added or available from __len__"
    assert coa.has_account(asset), "has_account method incorrectly returning"

    coa.remove_account(asset)
    assert len(coa) == 0, "Account not removed"

    coa.add_account("Test Account")
    assert len(coa) == 0, "Bad account was added"

    coa.add_account(asset)
    coa.remove_account("Test Asset")
    assert coa.has_account(asset), "Bad account name still removed an account"

    # Helper creation methods
    new_asset = coa.create_asset_account("New Asset", 25.0)
    assert coa.has_account(new_asset)

    new_liab = coa.create_liability_account("New Liability", 25.0)
    assert coa.has_account(new_liab)

    new_income = coa.create_income_account("New Income", 25.0)
    assert coa.has_account(new_income)

    new_expense = coa.create_expense_account("New Expense", 25.0)
    assert coa.has_account(new_expense)

    new_equity = coa.create_equity_account("New Equity", 35.0)
    assert coa.has_account(new_equity)


def test_coa_create_account(coa):
    """Test the create_account method on the ChartOfAccounts"""
    account = coa.create_and_add_account(
        account_type=AccountType.EXPENSE,
        account_name="Expense Account",
        starting_balance=55,
    )

    assert account, "No account returned from create_account"
    assert len(coa) == 1, "Account created not added to COA"
    assert (
        account == coa.accounts["EXPENSE"]["Expense Account"]
    ), "account was not indexed to the correct location"
    coa.remove_account(account)
    assert len(coa) == 0, "Created account not removed"

    account = coa.create_and_add_account(
        account_type="income", account_name="Good Account Type"
    )
    assert account, "Account not created by account_type string"
    coa.remove_account(account)

    account = coa.create_and_add_account(
        account_type="not_a_type", account_name="Bad Account Type"
    )
    assert not account, "Account shouldnt be created with a bad AccountType"
    assert len(coa) == 0, "Should not have added bad account"


def test_coa_by_name_and_type(coa, asset):
    """Tests the COA by_name_and_type method"""
    coa.add_account(asset)

    account = coa.by_name_and_type(asset.name, asset.account_type)
    assert account == asset, "COA by_name_and_type did not return the Account object"

    account = coa.by_name_and_type("Not in Here", "expense")
    assert not account, "Account returned when none exists with that name"

    account = coa.by_name_and_type("Test Account", "expense")
    assert not account, "Account returned when none exists in that account type"

    account = coa.by_name_and_type({}, 2)
    assert not account, "Account returned when garbage data given"


def test_transaction(filled_transaction):
    """Test creation and inspection of a transaction"""

    assert filled_transaction.total_debits == 20, "Debit not added correctly"
    assert filled_transaction.total_credits == 20, "Credit not added correctly"
    assert filled_transaction.n_entries == 2, "N_entries not correct"
    assert filled_transaction.is_balanced, "Balanced transaction shown as unbalanced"

    asset = filled_transaction.credits[0].account
    expense = filled_transaction.debits[0].account

    filled_transaction()

    assert expense.balance == 20, "Expense balance should be 20"
    assert asset.balance == 80


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

    transaction()

    assert asset.balance == 100

    transaction.clear()
    transaction.add_debit(asset)
    transaction.add_credit(asset)

    assert transaction.n_entries == 0
