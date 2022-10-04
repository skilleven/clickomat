import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

class Test_Pause_Class:

    def test_pause_with_int(self):
        line = "5"
        result = c._pause(line)
        assert result == 5

    def test_pause_with_float(self):
        line = "4.2"
        result = c._pause(line)
        assert result == 4.2

    def test_pause_with_longer_number(self):
        line = "42.2"
        result = c._pause(line)
        assert result == 42.2

    def test_pause_with_wrong_number(self):
        line = "42.244"
        result  = c._pause(line)
        assert result == 42.244

    def test_pause_with_zero(self):
        line = "0"
        result = c._pause(line)
        assert result == 0

    def test_pause_with_negative(self):
        line = "-1"
        result = c._pause(line)
        assert result == c.step_pause

