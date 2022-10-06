import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

class Test_findImages_Class:
# _findImages(self,line)
    def test_findImages_with_correct_line(self):
        image = ["D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png"]
        expected = 'D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png'
        result = c._findImages(image)
        assert result == expected

    def test_findImages_with_wrong_line(self):
        image = ["yyyyyy.png"]
        expected = False
        result = c._findImages(image)
        assert result == expected
