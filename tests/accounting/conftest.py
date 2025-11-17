import pytest
from tfin.accounting import Asset, Liability, Equity, Income, Expense

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