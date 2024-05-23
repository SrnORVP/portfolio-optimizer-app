from PortOpt.weights import get_len_of_combination
import pytest

from pydantic import ValidationError

from Server.app import ParseInput


@pytest.mark.xfail(raises=ValidationError)
@pytest.mark.serv
def test_server_parse1():
    # fail by start date input
    a = ParseInput(
        codes="0, 1,2,3,4,5,6,7,8,9,10",
        runs=500000,
        precision=1,
        start="2019-01-xx",
        end="2019-01-0x",
    )


@pytest.mark.xfail(raises=ValidationError)
@pytest.mark.serv
def test_server_parse2A():
    # fail at ratio check
    a = ParseInput(
        codes="0, 1,2,3",
        runs=10000,
        precision=2,
        start="2019-01-01",
        end="2019-02-01",
    )


@pytest.mark.serv
def test_server_parse2B():
    # bypass ratio check (ratio check always perform)
    a = ParseInput(
        ratio=False,
        codes="0, 1,2,3",
        runs=10000,
        precision=2,
        start="2019-01-01",
        end="2019-02-01",
    )

@pytest.mark.xfail(raises=ValidationError)
@pytest.mark.serv
def test_server_parse3():
    # fail at restriction check
    a = ParseInput(
        restricted=True,
        ratio=False,
        codes="0,1,2,3,4",
        runs=1000,
        precision=3,
        start="2019-01-01",
        end="2019-02-01",
    )


@pytest.mark.serv
def test_server_parse4():
    # bypass restriction check (restriction check is not always perform)
    a = ParseInput(
        ratio=False,
        codes="0,1,2,3,4",
        runs=1000,
        precision=3,
        start="2019-01-01",
        end="2019-02-01",
    )


@pytest.mark.serv
def test_possible_weight_limits():
    for p in range(1, 4):
        for e in range(3, 20):
            l = get_len_of_combination(e, p)
            if l > 500000:
                print(e, p, l)


@pytest.mark.xfail(raises=ValidationError)
@pytest.mark.serv
def test_data_parse():
    a = ParseInput(
        codes="0,1,2",
        runs=500000,
        precision=1,
        start="2019-01-01",
        end="2019-01-01",
    )

