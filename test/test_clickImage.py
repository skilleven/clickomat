import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

class Test_clickImage_Class:
    # test can only run in vscode because the image target is part of the vscode gui
    def test_clickImage(self):
        image = 'D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png'
        mode = 1
        expected = True
        result = c._clickImage(image,mode)
        assert result == expected
