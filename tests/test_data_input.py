import pytest


@pytest.mark.data
def test_mock(mocked_ef_no_change):
    ef = mocked_ef_no_change

    assert ef.data_value.shape[0] == 69
    assert ef.data_value.shape[0] == ef.data_index.shape[0]


@pytest.mark.data
def test_ret(mocked_ef_no_change):
    ef = mocked_ef_no_change
    ef.get_risk_return()

    for (k, v), (k1, v1) in zip(
        ef.stocks_daily_return.items(), ef.stocks_annual_return.items()
    ):
        # no ret afterall
        print(k, v, v1)
        assert k == k1
        assert v == 0
        assert v1 == 0
    # assert False


@pytest.mark.data
def test_std(mocked_ef_no_change):
    ef = mocked_ef_no_change
    assert ef.data_value.shape[0] == 69

    ef.get_risk_return()
    p = ef.YEARLY_PERIODS**0.5

    for (k, v), (k1, v1) in zip(
        ef.stocks_daily_risk.items(), ef.stocks_annual_risk.items()
    ):
        print(k, v * p, v1)
        assert k == k1
        assert v * p == v1
    # assert False

