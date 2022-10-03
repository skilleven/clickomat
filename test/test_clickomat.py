import pytest
import src as c

c = c.Clickomat('./testcases/checkboxolympics',
                't1.txt',
                'images')

c.test = True
c.logging = False

c._getClicklist()


"""
print(c.sections)

print(c._locateImage('D:/Projekte/clickomat/testcases/checkboxolympics/images/pytest.png'))
"""

