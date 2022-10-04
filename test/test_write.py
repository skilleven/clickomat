import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

class Test_write_Class:
    def test_write_normal(self):
        line = 'write "gds897HJKJHLHl ds df89s0 8s7hdsh ? "§$%&/()"'
        expected = True
        result = c._write(line)
        assert result == expected

    def test_write_shorthand(self):
        line = 'w "alle meine Entchen"'
        expected = True
        result = c._write(line)
        assert result == expected

    def test_write_wrong_quotes(self):
        line = "w 'alle meine Entchen'"
        expected = False
        result = c._write(line)
        assert result == expected
