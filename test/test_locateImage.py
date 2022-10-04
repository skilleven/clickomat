import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

class Test_locateImage_Class:
    # test can only run in vscode because the image target is part of the vscode gui
    def test_locateImage(self):
        image = 'D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png'
        expected = 'Box(left=5, top=5, width=66, height=24)'
        result = str(c._locateImage(image))
        assert result == expected

