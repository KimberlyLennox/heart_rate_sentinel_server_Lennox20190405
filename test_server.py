import pytest


@pytest.mark.parametrize("s, soln", [([100], "tachycardic"),
                                     ([80], "not tachycardic"),
                                     ([], "No heart rate data"
                                     " has been entered")])
def test_HRStatus(s, soln):
    from server import HRStatus
    ans = HRStatus(s)
    assert ans == soln


@pytest.mark.parametrize("s, soln", [([1, 2, 3, 4, 5, 6], 3.5),
                                     ([1], 1),
                                     ([], "No heart rate data "
                                      "has been entered")])
def test_Average(s, soln):
    from server import CalcAverage
    ans = CalcAverage(s)
    assert ans == soln


def test_CheckFormat1():
    from server import CheckFormat
    ans = "Patient saved successfully"
    data = {
            "patient_id": 1,
            "attending_email": "at@test.com",
            "user_age": 50
            }
    x = CheckFormat(data)
    assert ans == x


def test_CheckFormat2():
    from server import CheckFormat
    ans = "Incorrect format: please try again"
    data = {
            "patient_id": "1",
            "attending_email": 85,
            "user_age": "bob"
            }
    x = CheckFormat(data)
    assert ans == x


def test_CheckFormat3():
    from server import CheckFormat
    ans = "Incorrect format: please try again"
    data = {
            "attending_email": 85,
            "user_age": 12
            }
    x = CheckFormat(data)
    assert ans == x


def test_CheckHRData1():
    from server import CheckHRData
    data = {
            "patient_id": 1,
            "heart_rate": -1
            }
    x = CheckHRData(data)
    ans = "Incorrect format: please try again"
    assert x == ans


def test_CheckHRData2():
    from server import CheckHRData
    data = {
            "patient_id": 1,
            "heart_rate": 100
            }
    x = CheckHRData(data)
    ans = 0
    assert x == ans


def test_CheckHRData1():
    from server import CheckHRData
    data = {
            "patient_id": 1,
            "heart_rate": "Bob"
            }
    x = CheckHRData(data)
    ans = "Incorrect format: please try again"
    assert x == ans


def test_CheckIntervalData():
    from server import CheckIntervalData
    data = {
            "patient_id": 1,
            "heart_rate_since": "20190504"
            }
    x = CheckIntervalData(data)
    ans = "Incorrect format: please try again"
    assert x == ans
