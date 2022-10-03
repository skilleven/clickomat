import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics',
                't1.txt',
                'images')

c.test = True
c.logging = False


class Test_scroll_Class:
# _scroll(self,line)

    def test_scroll_with_correct_line(self):
        line = "scroll 5"
        expected = True
        result = c._scroll(line)
        assert result == expected

    def test_scroll_with_correct_neg_line(self):
        line = "scroll -5"
        expected = True
        result = c._scroll(line)
        assert result == expected

    def test_getSection_with_wrong_line(self):
        line = "scroll -xbvcx"
        expected = False
        result = c._scroll(line)
        assert result == expected

