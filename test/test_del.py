import pytest
import src as c
import os

if not os.path.exists('test3344'):
    with open('test3344', 'w'): pass
if not os.path.exists('test7644'):
    os.mkdir('test7644')

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_del_normal():
    line = 'del "test3344"'
    expected = 'delSuccess'
    result = c._del(line)
    assert result == expected

def test_del_fail():
    line = 'del "test334466"'
    expected = 'delFail'
    result = c._del(line)
    assert result == expected

def test_del_noPath():
    line = 'del fds"test334466"'
    expected = 'noPath'
    result = c._del(line)
    assert result == expected

def test_del_dir():
    line = 'del dir "test7644"'
    expected = 'delDirSuccess'
    result = c._del(line)
    assert result == expected