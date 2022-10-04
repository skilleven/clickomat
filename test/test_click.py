import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_click_normal_click():
    line, mode = "click", 1
    expected = 'normalClickExecuted'
    result = c._click(line, mode)
    assert result == expected

def test_click_normal_click2():
    line, mode = "c", 1
    expected = 'normalClickExecuted'
    result = c._click(line, mode)
    assert result == expected

def test_click_normal_dclick():
    line, mode = "doubleclick", 2
    expected = 'normalDoubleClickExecuted'
    result = c._click(line, mode)
    assert result == expected

def test_click_normal_dclick2():
    line, mode = "dc", 2
    expected = 'normalDoubleClickExecuted'
    result = c._click(line, mode)
    assert result == expected

def test_click_normal_sclick():
    line, mode = "shiftclick", 3
    expected = 'normalShiftClickExecuted'
    result = c._click(line, mode)
    assert result == expected

def test_click_normal_sclick2():
    line, mode = "sc", 3
    expected = 'normalShiftClickExecuted'
    result = c._click(line, mode)
    assert result == expected

def test_click_normal_imageNotFound():
    line, mode = "c -dfgdf", 1
    expected = 'imageNotFound'
    result = c._click(line, mode)
    assert result == expected

def test_click_normal_image():
    line, mode = "click -pytest", 1
    expected = 'ImgClick_ClickExecuted'
    result = c._click(line, mode)
    assert result == expected

def test_click_normal_imageNotFound():
    line, mode = "c -first-ff", 1
    expected = 'ImgClick_could_not_be_executed'
    result = c._click(line, mode)
    assert result == expected

def test_click_normal_imageNotFound():
    line, mode = "c ! -first-ff", 1
    expected = 'ImgClick_could_not_be_executed'
    result = c._click(line, mode)
    assert result == expected