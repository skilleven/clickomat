import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False
c._getClicklist()

def test_if_normal():
    line = 'if -pytest ->MAIN'
    expected = 'success'
    result = c._if(line)
    assert result == expected

def test_if_no_section():
    line = 'if -pytest'
    expected = 'fail'
    result = c._if(line)
    assert result == expected

def test_if_no_image():
    line = 'if ->MAIN'
    expected = 'fail'
    result = c._if(line)
    assert result == expected

def test_image_not_found():
    line = 'if -first-ff ->MAIN'
    expected = 'fail'
    result = c._if(line)
    assert result == expected

def test_go_normal():
    line = 'go ->MAIN'
    expected = 'success'
    result = c._go(line)
    assert result == expected

def test_go_normal2():
    line = 'go ->#MAIN'
    expected = 'success'
    result = c._go(line)
    assert result == expected

def test_go_no_section():
    line = 'go'
    expected = 'fail'
    result = c._go(line)
    assert result == expected


