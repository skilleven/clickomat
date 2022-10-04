import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_getPath_normal():
    line = 'del "D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png"'
    expected = "D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png"
    result = c._getPath(line)
    assert result == expected


def test_getPath_wrong():
    line = 'del D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png'
    expected = False
    result = c._getPath(line)
    assert result == expected

