import sys
sys.path.append('../../')
from clickomat import *
c = Clickomat('.','t1.txt',"images")
c.step_pause = 0.02
c.logging = True
c.autoswitch = True
c.autoswitch_pause = 5
c.main()