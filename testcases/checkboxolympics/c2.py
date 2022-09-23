import sys
sys.path.append('../../')
from clickomat import *

input_file = """
switch
await -refresh

click ! -refresh
await -ready/ready_mac
click ! -ready/ready_mac
await -go/go_mac
1
click -first
right 20
click
right 20
click
right 20
click
right 20
click
right 25
click
right 20
click
right 20
click
right 25
click
right 20
click
right 20
click
right 20
click
right 20
click
right 23
click
right 20
click
right 20
click
right 23
click
right 20
click
right 20
click
right 20
click
right 25
click
right 20
click
right 20
click
right 20
click
right 20
click
right 24
click
right 20
click
right 20
click
"""
c = Clickomat('.',input_file,"images")
c.step_pause = 0.02
c.logging = True
c.autoswitch = True
c.autoswitch_pause = 5
c.main()