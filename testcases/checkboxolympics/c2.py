import sys
sys.path.append('../../src/')
from clickomat import *

input_file = """
switch

await -refresh
click -refresh-ff/refresh-chrome-win

await --ready-ff-win/ready-ff-mac/ready-chrome-win
click ! -ready-ff-win/ready-ff-mac/ready-chrome-win

await -go-ff-win/go-ff-mac/go-chrome-win
2
click -first-ff/first-chrome-win

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