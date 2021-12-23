from src.model.cashFlowManagement import addNewCashFlow, getCashflowsByUserID, get10RecentCashflowsByUserID, deleteCashFlow, deleteCashFlowByUserID
from src.model.makeDatabaseConnection import makeDatabaseConnection


def test_():
    db = makeDatabaseConnection()
    cashFlow = getCashflowsByUserID(db, 123)
    if cashFlow is not None:
        assert deleteCashFlowByUserID(db, 123) is True
    assert addNewCashFlow(db, 123, 100, "转账") is True
    assert addNewCashFlow(db, 123, -50, "转账") is True
    cashflow = getCashflowsByUserID(db, 123)
    cashFlow10Result = get10RecentCashflowsByUserID(db, 123, "转账")
    assert len(cashFlow10Result) == 2
    assert cashflow is not None
    assert len(cashflow) == 2
    assert deleteCashFlow(db, cashflow[0][0]) is True
    assert deleteCashFlow(db, cashflow[1][0]) is True
    db.close()