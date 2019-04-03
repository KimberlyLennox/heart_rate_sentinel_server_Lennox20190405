import pytest


@pytest.mark.parametrize("s, soln", [([100], "tachycardic"),
                                     ([80], "not tachycardic"),
                                     ([], "None")])
def test_HRStatus(s, soln):
    from server import HRStatus
    ans = HRStatus(s)
    assert ans == soln
