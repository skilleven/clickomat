import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_drag_normal():
    line = "drag -pytest"
    expected = 'dragSuccess'
    result = c._drag(line)
    assert result == expected

def test_drag_up():
    line = "drag up -pytest"
    expected = 'dragUpSuccess'
    result = c._drag(line)
    assert result == expected

def test_drag_image_not_existing():
    line = "drag -turd"
    expected = 'imageNotFound'
    result = c._drag(line)
    assert result == expected

def test_drag_no_target():
    line = "drag"
    expected = 'nothingToDrag'
    result = c._drag(line)
    assert result == expected

def test_drag_up_no_target():
    line = "drag up"
    expected = 'nothingToDrag'
    result = c._drag(line)
    assert result == expected

