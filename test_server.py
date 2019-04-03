import pytest


@pytest.mark.parametrize("s, soln", [([100], "tachycardic"),
                                     ([80], "not tachycardic"),
                                     ([], "None")])
def test_HRStatus(s, soln):
    from server import HRStatus
    ans = HRStatus(s)
    assert ans == soln


@pytest.mark.parametrize("s, soln", [([1, 2, 3, 4, 5, 6], 3.5),
                                     ([1], 1),
                                     ([], 0)])
def test_Average(s, soln):
    from server import CalcAverage
    ans = CalcAverage(s)
    assert ans == soln
