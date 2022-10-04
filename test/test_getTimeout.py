import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

class Test_getTimeout_Class:
# _getTimeout(self,line)

    def test_getTimeout_with_correct_line(self):
        line = "await 5 -refresh-ff"
        expected = 5
        result = c._getTimeout(line)
        assert result == expected

    def test_getTimeout_with_wrongISH_line(self):
        line = "await ztrr -refresh-ff"
        expected = 10
        result = c._getTimeout(line)
        assert result == expected

    def test_getTimeout_with_noTimeout_line(self):
        line = "await -refresh-ff"
        expected = 10
        result = c._getTimeout(line)
        assert result == expected

    def test_getTimeout_with_akward_line(self):
        line = "await 34.67 -refresh-ff"
        expected = 10
        result = c._getTimeout(line)
        assert result == expected

    def test_getTimeout_with_akward_line(self):
        line = "await -10 -refresh-ff"
        expected = 10
        result = c._getTimeout(line)
        assert result == expected

