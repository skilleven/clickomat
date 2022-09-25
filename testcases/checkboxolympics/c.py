import sys
sys.path.append('../../src/')
from clickomat import *
c = Clickomat('.','t1.txt',"images")
c.step_pause = 0.03
c.logging = True
c.autoswitch = False
c.autoswitch_pause = 5
c.confidence = 0.8

c.main()