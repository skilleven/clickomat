import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_pop():
    line = 'pop "This is a test message"'
    expected = True
    result = c._pop(line)
    assert result == expected

def test_pop2():
    line = 'pop'
    expected = False
    result = c._pop(line)
    assert result == expected


