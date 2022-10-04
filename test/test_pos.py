import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_pos_normal_line():
    line = "pos -pytest"
    expected = 'positionedSuccessful'
    result = c._pos(line)
    assert result == expected

def test_pos_target_not_found():
    line = "pos -first-ff"
    expected = 'positionFail'
    result = c._pos(line)
    assert result == expected

def test_pos_image_not_existing():
    line = "pos -turd"
    expected = 'imageNotFound'
    result = c._pos(line)
    assert result == expected

