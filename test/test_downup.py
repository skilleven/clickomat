import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_mDownUp_normal_md():
    line = "mdown"
    expected = "mdown"
    result = c._mDownUp(line)
    assert result == expected

def test_mDownUp_normal_md2():
    line = "md"
    expected = "mdown"
    result = c._mDownUp(line)
    assert result == expected

def test_mDownUp_normal_mu():
    line = "mup"
    expected = "mup"
    result = c._mDownUp(line)
    assert result == expected

def test_mDownUp_normal_mu2():
    line = "mu"
    expected = "mup"
    result = c._mDownUp(line)
    assert result == expected
