import pytest
import src as c


c = c.Clickomat('./testcases/checkboxolympics',
                't1.txt',
                'images')

c._getClicklist()

# print(c.sections)

# Fake Data:
# c.sections[section]

class Test_Pause_Class:
# _pause(self,line)

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

class Test_getImage_Class:
# _getImage(self,line)

    def test_getImage_with_correct_line(self):
        line = "click -first-ff"
        expected = ['./testcases/checkboxolympics/images/first-ff.png']
        result = c._getImage(line)
        assert result == expected

    def test_getImage_with_correct_line_2_images(self):
        line = "click -first-ff/first-chrome-win"
        expected = [
                    './testcases/checkboxolympics/images/first-ff.png',
                    './testcases/checkboxolympics/images/first-chrome-win.png',
                ]
        result = c._getImage(line)
        assert result == expected

    def test_getImage_with_non_existing_image(self):
        line = "click -nonsense"
        expected = False
        result = c._getImage(line)
        assert result == expected

    def test_getImage_with_non_existing_images(self):
        line = "click -nonsense/rubbish"
        expected = False
        result = c._getImage(line)
        assert result == expected

    def test_getImage_with_no_image(self):
        line = "click"
        expected = "Click"
        result = c._getImage(line)
        assert result == expected

class Test_getSection_Class:
# _getSection(self,line)

    def test_getSection_with_correct_line(self):
        line = "go ->SECTION1MILL"
        expected = "SECTION1MILL"
        result = c._getSection(line)
        assert result == expected

    def test_getSection_with_arrow_space(self):
        line = "go -> SECTION1MILL"
        expected = "SECTION1MILL"
        result = c._getSection(line)
        assert result == expected

    def test_getSection_with_hash(self):
        line = "go -> #SECTION1MILL"
        expected = "SECTION1MILL"
        result = c._getSection(line)
        assert result == expected

    def test_getSection_with_hashes(self):
        line = "go -> ##SECTION1MILL"
        expected = "SECTION1MILL"
        result = c._getSection(line)
        assert result == expected

    def test_getSection_with_non_existing_section(self):
        line = "go ->NONSENSE"
        expected = False
        result = c._getSection(line)
        assert result == expected









