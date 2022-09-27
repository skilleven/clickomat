from clickomat import Clickomat
c = Clickomat('.','t1.txt',"images")
# c.switch = False <- you can turn off switch commands completely
c.step_pause = 0.03
c.logging = True
c.autoswitch = False
c.autoswitch_pause = 5
c.confidence = 0.8

c.main()