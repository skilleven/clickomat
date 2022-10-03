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
