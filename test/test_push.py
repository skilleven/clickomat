import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_push_right():
    order = ["right",20]
    expected = 'right'
    result = c._push(order)
    assert result == expected

def test_push_left():
    order = ["left",20]
    expected = 'left'
    result = c._push(order)
    assert result == expected

def test_push_up():
    order = ["up",20]
    expected = 'up'
    result = c._push(order)
    assert result == expected

def test_push_down():
    order = ["down",20]
    expected = 'down'
    result = c._push(order)
    assert result == expected

def test_push_wrong():
    order = ["wrong",20]
    expected = False
    result = c._push(order)
    assert result == expected

