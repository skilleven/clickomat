import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_await_normal():
    line = "await -pytest"
    expected = 'imageFound'
    result = c._await(line)
    assert result == expected

def test_await_normal_moretime():
    line = "await 5 -pytest"
    expected = 'imageFound'
    result = c._await(line)
    assert result == expected

def test_await_normal_lesstime():
    line = "await 0 -pytest"
    expected = 'imageNotFound'
    result = c._await(line)
    assert result == expected

def test_await_fail():
    line = "await -first-ff"
    expected = 'imageNotFound'
    result = c._await(line)
    assert result == expected

