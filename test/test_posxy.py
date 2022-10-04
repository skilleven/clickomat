import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_posxy_normal_x():
    line, mode = "x 20", 'x'
    expected = True
    result = c._posxy(line, mode)
    assert result == expected

def test_posxy_normal_y():
    line, mode = "y 20", 'y'
    expected = True
    result = c._posxy(line, mode)
    assert result == expected

def test_posxy_err1():
    line, mode = "y", 'y'
    expected = False
    result = c._posxy(line, mode)
    assert result == expected
