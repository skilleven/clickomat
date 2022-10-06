import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False

class Test_getImages_Class:
# _getImages(self,line)

    def test_getImages_with_correct_line(self):
        line = "click -first-ff"
        expected = ['./testcases/checkboxolympics/images/first-ff.png']
        result = c._getImages(line)
        assert result == expected

    def test_getImages_with_correct_line_2_images(self):
        line = "click -first-ff/first-chrome-win"
        expected = [
                    './testcases/checkboxolympics/images/first-ff.png',
                    './testcases/checkboxolympics/images/first-chrome-win.png',
                ]
        result = c._getImages(line)
        assert result == expected

    def test_getImages_with_non_existing_image(self):
        line = "click -nonsense"
        expected = False
        result = c._getImages(line)
        assert result == expected

    def test_getImages_with_non_existing_images(self):
        line = "click -nonsense/rubbish"
        expected = False
        result = c._getImages(line)
        assert result == expected

    def test_getImages_with_no_image(self):
        line = "click"
        expected = "Click"
        result = c._getImages(line)
        assert result == expected
