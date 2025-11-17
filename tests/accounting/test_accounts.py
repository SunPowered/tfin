from tfin.accounting import Asset, Account, accounts_by_type, AccountType, Income

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