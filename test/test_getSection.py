import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics','t1.txt','images')
c.test = True
c.logging = False
c._getClicklist()

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

class Test_locateImage_Class:
    # test can only run in vscode because the image target is part of the vscode gui
    def test_locateImage(self):
        image = 'D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png'
        expected = 'Box(left=5, top=5, width=66, height=24)'
        result = str(c._locateImage(image))
        assert result == expected

class Test_clickImage_Class:
    # test can only run in vscode because the image target is part of the vscode gui
    def test_clickImage(self):
        image = 'D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png'
        mode = 1
        expected = True
        result = c._clickImage(image,mode)
        assert result == expected

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
