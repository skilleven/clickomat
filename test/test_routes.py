import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

def test_clickRoute():
    command = "click"
    line    = "click -pytest"
    expected = f"self._click('{line}',1)"
    result = c._clickRoute(command,line)
    assert result == expected

def test_clickRoute2():
    command = "doubleclick"
    line    = "dc -pytest"
    expected = f"self._click('{line}',2)"
    result = c._clickRoute(command,line)
    assert result == expected

def test_pushRoute():
    command = "right"
    order = "order"
    expected = f"self._push({order})"
    result = c._pushRoute(command,order)
    assert result == expected

def test_screenshot():
    command = "screenshot"
    expected = 'self._screenshot()'
    result = c._routes(command)
    assert result == expected

def test_drag():
    command = "drag"
    expected = 'self._drag(line)'
    result = c._routes(command)
    assert result == expected

def test_mdown():
    command = "mdown"
    expected = 'self._mDownUp(line)'
    result = c._routes(command)
    assert result == expected

def test_mdown2():
    command = "md"
    expected = 'self._mDownUp(line)'
    result = c._routes(command)
    assert result == expected

def test_mup():
    command = "mup"
    expected = 'self._mDownUp(line)'
    result = c._routes(command)
    assert result == expected

def test_mup2():
    command = "mu"
    expected = 'self._mDownUp(line)'
    result = c._routes(command)
    assert result == expected

def test_pos():
    command = "pos"
    expected = 'self._pos(line)'
    result = c._routes(command)
    assert result == expected

def test_posX():
    command = "posX"
    expected = "self._posxy(line,'x')"
    result = c._routes(command)
    assert result == expected

def test_posX2():
    command = "X"
    expected = "self._posxy(line,'x')"
    result = c._routes(command)
    assert result == expected

def test_posX3():
    command = "x"
    expected = "self._posxy(line,'x')"
    result = c._routes(command)
    assert result == expected

def test_posY():
    command = "posY"
    expected = "self._posxy(line,'y')"
    result = c._routes(command)
    assert result == expected

def test_posX2():
    command = "Y"
    expected = "self._posxy(line,'y')"
    result = c._routes(command)
    assert result == expected

def test_posX3():
    command = "y"
    expected = "self._posxy(line,'y')"
    result = c._routes(command)
    assert result == expected

def test_if():
    command = "if"
    expected = "self._if(line)"
    result = c._routes(command)
    assert result == expected

def test_go():
    command = "go"
    expected = "self._go(line)"
    result = c._routes(command)
    assert result == expected

def test_await():
    command = "await"
    expected = "self._await(line)"
    result = c._routes(command)
    assert result == expected

def test_await2():
    command = "a"
    expected = "self._await(line)"
    result = c._routes(command)
    assert result == expected

def test_write():
    command = "write"
    expected = "self._write(line)"
    result = c._routes(command)
    assert result == expected

def test_write2():
    command = "w"
    expected = "self._write(line)"
    result = c._routes(command)
    assert result == expected

def test_enter():
    command = "enter"
    expected = "keyboard.press('enter')"
    result = c._routes(command)
    assert result == expected

def test_enter2():
    command = "."
    expected = "keyboard.press('enter')"
    result = c._routes(command)
    assert result == expected

def test_scroll():
    command = "scroll"
    expected = "self._scroll(line)"
    result = c._routes(command)
    assert result == expected

def test_scroll2():
    command = "sl"
    expected = "self._scroll(line)"
    result = c._routes(command)
    assert result == expected

def test_del():
    command = "del"
    expected = "self._del(line)"
    result = c._routes(command)
    assert result == expected

def test_del2():
    command = "d"
    expected = "self._del(line)"
    result = c._routes(command)
    assert result == expected

def test_deldir():
    command = "dd"
    expected = "self._del(line,'dir')"
    result = c._routes(command)
    assert result == expected

def test_pop():
    command = "pop"
    expected = "self._pop(line)"
    result = c._routes(command)
    assert result == expected










