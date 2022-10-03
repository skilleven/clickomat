import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False
c._getClicklist()

class Test_findImage_Class:
# _findImage(self,line)
    def test_findImage_with_correct_line(self):
        image = ["D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png"]
        expected = 'D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png'
        result = c._findImage(image)
        assert result == expected
        
    def test_findImage_with_wrong_line(self):
        image = ["yyyyyy.png"]
        expected = False
        result = c._findImage(image)
        assert result == expected
