import pyautogui, re, time, keyboard, os, shutil, click # type: ignore
from tkinter import *
import tkinter.messagebox as tkmb
from datetime import datetime
from os.path import exists
from datetime import datetime
if os.name == 'nt': import msvcrt

#-----------------------------------------------------
#
# Clickomat v0.3.0
#
#-----------------------------------------------------

class Clickomat:
    # region __init__
    def __init__(self, case_path=None, input_file=None, images=None):
        self.commands = None
        if case_path is None:
            self.case_path = "."
        else:
            self.case_path = case_path
            if not os.path.isdir(self.case_path):
                print(self.case_path)
                print("given case path is not existing.")
                exit()

        if input_file is None:
            self.input_file = "t1.txt"
        else:
            self.input_file = input_file
            if ".txt" not in self.input_file:
                # this means there was not a txt file specified
                # but an actual list (lines) of commands
                self.commands = self.input_file
            else:
                self.input_file = f"{self.case_path}/{self.input_file}"
                if not exists(self.input_file):
                    print(self.input_file)
                    print("given clicklist is not existing.")
                    exit()

        if images is None:
            self.images = "."
        else:
            self.images = f"{self.case_path}/{images}"

            if not os.path.isdir(self.images):
                print(self.input_file)
                print("given image location is not existing.")
                exit()

        self.confidence           = 0.95
        self.autoswitch           = False
        self.autoswitch_pause     = 1

        self.logging              = True
        self.step_pause           = 0.06
        self.switch_pause         = 0
        self.switched             = 0
        self.switch               = True

        self.breakout             = False
        self.stopped              = False
        self.error                = ""

        self.lookupTarget         = []

    # endregion
    # region _pause(line)
    def _pause(self,line):
        if line == ".": return
        if len(line) < 4:
            pause = re.search(r"^[0-9\.]+$", line)
            if pause:
                pause = pause.group(0)
                return float(pause)
            else:
                return self.sp()

        else:
            return self.sp()

    def sp(self):
        if self.step_pause > 0:
            return float(self.step_pause)
        else:
            return False
    # endregion
    # region _getImage(line)
    def _getImage(self,line):
        needle = " -[a-zA-Z0-9_\-/]+"
        img = False
        result = []
        try: img = re.search(needle, line).group(0)
        except: return "Click"

        try:
            img = re.search(needle, line).group(0)
            img = img[2:len(img)]
            img = img.split("/")

            for i in img:
                this = f"{self.images}/{i}.png"
                if exists(this):
                    result.append(this)

            if not len(result):
                return False

            return result

        except:
            return False
    # endregion
    # region _getSection(line)
    def _getSection(self,line):
        needle = r"->[a-zA-Z0-9_\-]+"
        section = False
        try:
            section = re.search(needle, line).group(0)
        except:
            print("no section found")
            return False
        try:
            section = re.search(needle, line).group(0)
            section = section[2:len(section)]
            if self.sections[section]:
                return section
        except:
            return False
    # endregion
    # region _scroll(line)
    def _scroll(self,line):
        try:
            amount = re.search(r" -?[0-9]+", line).group(0)
            amount = amount[1:len(amount)]
            amount = int(amount)
            pyautogui.scroll(amount)
            return True
        except:
            return False
    # endregion
    # region _getTimeout(line)
    def _getTimeout(self,line):
        try:
            timeout = re.search(r" [0-9]+ ", line).group(0)
            return int(timeout)
        except:
            return 10
    # endregion
    # region _findImage(image)
    def _findImage(self,image):
        x = False
        for i in image:
            try:
                x, y = pyautogui.locateCenterOnScreen(i, confidence=self.confidence)
            except: pass
            if x: return i
        return False
    # endregion
    # region _locateImage(image)
    def _locateImage(self,image):
        try:
            box = pyautogui.locateOnScreen(image, confidence=self.confidence)
            return box
        except:
            return False
    # endregion
    # region _clickImage(image,mode)
    def _clickImage(self,image,mode):
        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence=self.confidence)
            if mode == 1: pyautogui.click(x, y)
            if mode == 2: pyautogui.doubleClick(x, y)
            if mode == 3: self._shiftclick(x, y)

            
            return True
        except:
            return False
    # endregion
    # region _switch()
    def _switch(self):
        if os.name == 'nt':
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.keyUp('alt')
        else:
            pyautogui.keyDown('command')
            pyautogui.press('tab')
            pyautogui.keyUp('command')
        if self.switch_pause > 0:
            time.sleep(self.switch_pause)
    # endregion
    # region _write(line)
    def _write(self,line):
        try:
            text = re.search(r" \"[a-zA-Z0-9_:\-\.\/\\]+\"", line).group(0)
            text = text[2:len(text)-1]
            if self.logging: print(" -> ", text, end = "")
            keyboard.write(text)
            return True
        except:
            if self.logging: print(" -> not written.", end = "")
            self.error = "Text could not be written"
            self.breakout = True
            return False
    # endregion
    # region _getPath(line)
    def _getPath(self,line):
        try:
            path = re.search(r" \"[a-zA-Z0-9_:\-\.\/\\]+\"", line).group(0)
            path = path[2:len(path)-1]
            return path
        except:
            return False
    # endregion
    # region _stop()
    def _stop(self):
        self.stopped = True
    # endregion
    # region _imageNotFound()
    def _imageNotFound(self):
        self.error = "Target image not existing!"
        if self.logging: print(" -> Target image not existing! Check directory for screenshot-snippet.", end = "")
    # endregion
    # region _push(order)
    def _push(self,order):
        amount = int(order[1])
        if order[0] == "up":    pyautogui.moveRel(0,amount*-1)
        if order[0] == "down":  pyautogui.moveRel(0,amount)
        if order[0] == "right": pyautogui.moveRel(amount,0)
        if order[0] == "left":  pyautogui.moveRel(amount*-1,0)
    # endregion
    # region _click(line,mode)
    def _click(self,line,mode):
            image = self._getImage(line)
            if image != "Click":
                image = self._findImage(image)

            if image == "Click":
                if mode==1: 
                    pyautogui.click()
                    if self.logging: print(" -> clicked!", end="")

                if mode==2: 
                    pyautogui.doubleclick()
                    if self.logging: print(" -> doubleclicked!", end="")

                if mode==3: 
                    self._shiftclick()
                    if self.logging: print(" -> shift-clicked!", end="")

            else:
                if not image:
                    self._imageNotFound()

                if not self._clickImage(image,mode):
                    if self.logging: print(" -> not clicked!", end="")

                    order = line.split(" ")

                    if " ! " in order:
                        if self.logging: print()
                        self.error = "Forced image-click could not be executed"
                        if self.logging: print("Loop Broke!\n\n")
                        self.breakout = True
                        return
                else:
                    if self.logging:
                        if mode==1: 
                            print(" -> clicked!", end="") 
                        if mode==2: 
                            print(" -> doubleclicked!", end="")
                        if mode==3: 
                            print(" -> shift-clicked!", end="")
    # endregion
    # region _pos(line)
    def _pos(self,line):
                image = self._getImage(line)[0]
                if not image:
                    self._imageNotFound()
                    return
                box = self._locateImage(image)
                if box:
                    if self.logging: print(" -> ", box, end = "")
                    pyautogui.moveTo((box[0]+(box[2]/2)),(box[1]+(box[3]/2)))
                else:
                    if self.logging: print(" -> Position not found!", end="")
                    self.error = "Position not found!"
                    self.breakout = True
    # endregion
    # region _posy(line)
    def _posxy(self,line,mode):
        needle = r" [0-9]+"
        x, y = pyautogui.position()
        try:
            if mode == 'y': y = int(re.search(needle, line).group(0)[1:])
            if mode == 'x': x = int(re.search(needle, line).group(0)[1:])
        except:
            print("no value assigned!")
            return False
        try:
            pyautogui.moveTo(x,y)
            return True
        except:
            return False
    # endregion
    # region _mDownUp(line)
    def _mDownUp(self,line):
        if line == "mdown" : pyautogui.mouseDown()
        if line == "md"    : pyautogui.mouseDown()
        if line == "mup"   : pyautogui.mouseUp()
        if line == "mu"    : pyautogui.mouseUp()
    # endregion
    # region _drag(line)
    def _drag(self,line):
        order = line.split(" ")
        image = self._getImage(line)[0]
        if not image:
            self._imageNotFound()
            return
        box = self._locateImage(image)
        if box:
            if self.logging: print(" -> ", box, end = "")

            if "up" in order:
                pyautogui.moveTo((box[0]),(box[1]+box[3]))
                pyautogui.dragTo((box[0]+box[2]),(box[1]), button='left')
            else:
                pyautogui.moveTo(box[0],box[1])
                pyautogui.dragTo((box[0]+box[2]),(box[1]+box[3]), button='left')
        else:
            if self.logging: print(" -> nothing to drag!", end="")
            self.error = "Nothing to drag!"
            self.breakout = True
    # endregion
    # region _await(line)
    def _await(self,line):
        found = False
        timeout = self._getTimeout(line)
        if self.logging: print(" -> timeout: " + str(timeout) + "s", end = "")
        start_time = datetime.now()

        image = self._getImage(line)

        if not image:
            self._imageNotFound()
        else:
            if self.logging: print(f" on {str(image)}", end = "")

            while 1:
                self._stopLoop()
                time_delta = datetime.now() - start_time
                if time_delta.total_seconds() >= timeout:
                    break

                if self._findImage(image):
                    t=round(time_delta.total_seconds())
                    if self.logging: print(" -> found after " + str(t) + "s.",end = "")
                    found = True
                    break

            if not found:
                if self.logging: print(" -> Not found.", end = "")
                self.error = "Image to wait for was not found."
                self.breakout = True
    # endregion
    # region _del(line)
    def _del(self,line,mode="file"):

        order = line.split(" ")

        if "dir" in order:
            mode = "dir"

        path = self._getPath(line)

        if not path: return

        if mode == "file":
            try:
                os.remove(path)
            except OSError as e:
                print(e)
            else:
                print("The File is deleted successfully", end = "")

        if mode == "dir":
            try:
                shutil.rmtree(path)
            except OSError as e:
                print(e)
            else:
                print("The directory is deleted successfully", end = "")

    # endregion
    # region _stopLoop()
    def _stopLoop(self):
        self._abort()
        if self.breakout:
            if self.logging: print ("Loop broken!\n\n")
            message = "An error has occured: " + self.error
            self._popupMessage(message,'error')
            exit()
        if self.stopped:
            if self.logging: print ("Loop stopped!\n\n")
            exit()
    # endregion
    # region _end()
    def _end(self):
        message = "The script is finished!"
        self._popupMessage(message)
    # endregion
    # region _setLookup()
    def _setLookup(self,line):
        if self.logging: print("Set Lookup!", end=" -> ")
        # only one image can be used for lookup so far...
        image   = self._getImage(line)[0]
        sec     = self._getSection(line)
        if image and sec:
            self.lookupTarget = [image,sec]
        if self.logging: print(self.lookupTarget)
        # print(self.lookupTarget)
        return
    # endregion
    # region _checkLookup()
    def _checkLookup(self):
        if len(self.lookupTarget):
            if self._findImage([self.lookupTarget[0]]):
                self.section = self.lookupTarget[1]
                if self.logging: print("\nImage lookup found -> Go Section {self.section}!\n")
                self.ClickLoop(self.section)
    # endregion
    # region _if(line)
    def _if(self,line):
        image = self._getImage(line)
        sec = self._getSection(line)
        if self._findImage(image):
            if self.logging: print(f"\nImage (if) found -> Go Section {sec}!\n")
            self.section = sec
            self.ClickLoop(self.section)
    # endregion
    # region _go(line)
    def _go(self,line):
        sec = self._getSection(line)
        if sec:
            if self.logging: print(f"\nGo Section {sec}!\n")
            self.section = sec
            self.ClickLoop(self.section)
    # endregion
    # region _abort()
    def _abort(self):
        try:
            if msvcrt.kbhit() and msvcrt.getch().decode() == chr(27):
                exit()
        except:
            pass
    # endregion
    # region _popupMessage(message,t='info') t -> type
    def _popupMessage(self,message,t='info'):
        title = "Clickomat"
        if t == "info":    tkmb.showinfo(title=title, message=message)
        if t == "error":   tkmb.showerror(title=title, message=message)
        if t == "warning": tkmb.showwarning(title=title, message=message)
    # endregion
    # region _screenshot()
    def _screenshot(self):
        dest = self.case_path + '/screenshots'
        if not os.path.exists(dest):
            # if the screenshot folder directory is not present
            # then create it.
            os.makedirs(dest)
        now = datetime.now()
        timestamp = str(now.strftime("%Y%m%d_%H-%M-%S"))
        filename = f"{dest}/screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
    # endregion
    # region _shiftclick(x,y)
    def _shiftclick(self,x=None,y=None):
        pyautogui.keyDown('shift')
        if not x and not y:
            pyautogui.click()
        else:
            pyautogui.click(x,y)
        pyautogui.keyUp('shift')
    #end region
    
    # region main()
    def main(self):

        if self.logging: print(f"Case Path: {self.case_path}")
        if self.logging: print(f"Clicklist: {self.input_file}")
        if self.logging: print(f"Image Directory: {self.images}")
        if self.logging: print("---")

        if self.commands is not None:
            lines = iter(self.commands.splitlines())
        else:
            with open(self.input_file, 'r', encoding='UTF-8') as file:
                lines = file.readlines()

        lines = [line.rstrip() for line in lines]

        self.sections = {}
        self.section = "SECTION1"
        self.sections[self.section] = []

        for linenumber, line in enumerate(lines, start=1):
            if line[:2] == "##":
                self.section = line[2:]
                self.sections[self.section]= []
                continue
            if line:
                line = [linenumber,line]
                self.sections[self.section].append(line)

        self.section = list(self.sections.keys())[0]

        pyautogui.PAUSE = 0
        if self.logging: print("\n\n\n\n\n---------------------------------------------------")

        self.ClickLoop(self.section)

        if not self.breakout:
            if self.logging: print()
            if self.logging: print ("Loop finished.\n\n")
    # endregion
    
    # region Clickloop
    def ClickLoop(self,sec):

        self.lookupTarget = []
        if self.logging: print(f"Running section: {sec}")

        for line in self.sections[sec]:

            if sec != self.section: break
            lnr  = line[0]
            line = line[1]

            if self.logging: print()

            p = self._pause(line)
            if p: time.sleep(p)

            self._stopLoop()

            if self.logging: print(lnr, end = " " )
            if self.logging: print(line, end = "" )

            if sec != self.section: break

            order   = line.split(" ")
            command = order[0]

            if command == "#": continue

            if command == "lookup" or command == "lu": self._setLookup(line)

            self._checkLookup()

            if sec != self.section: break

            if command == "stop": 
                self._stop()
                break

            if command == "switch" or command == ">":
                if self.switch or "!" in order:
                    self._switch()
                    self.switched += 1
                continue

            if sec != self.section: break
            self._stopLoop()

            if (command=="right" or command=="left" or command=="up" or command=="down") \
            or (command=="r"     or command=="l"    or command=="u"  or command=="d")    : 
                self._push(order)
                continue

            if command=="click" \
            or command=="doubleclick" \
            or command=="shiftclick" \
            or command=="c" or command=="dc" or command=="sc":
                if command=="click" or command=="c"        : mode = 1
                if command=="doubleclick" or command=="dc" : mode = 2
                if command=="shiftclick" or command=="sc"  : mode = 3
                self._click(line,mode)
                continue

            self._stopLoop()
            if command == "screenshot": self._screenshot()       ;continue
            if command == "shot"      : self._screenshot()       ;continue
            if command == "drag"      : self._drag(line)         ;continue
            if command == "mdown"     : self._mDownUp(line)      ;continue
            if command == "md"        : self._mDownUp(line)      ;continue
            if command == "mup"       : self._mDownUp(line)      ;continue
            if command == "mu"        : self._mDownUp(line)      ;continue
            if command == "pos"       : self._pos(line)          ;continue
            if command == "posX"      : self._posxy(line,'x')    ;continue
            if command == "X"         : self._posxy(line,'x')    ;continue
            if command == "x"         : self._posxy(line,'x')    ;continue
            if command == "posY"      : self._posxy(line,'y')    ;continue
            if command == "Y"         : self._posxy(line,'y')    ;continue
            if command == "y"         : self._posxy(line,'y')    ;continue
            if command == "if"        : self._if(line)           ;continue
            if command == "go"        : self._go(line)           ;continue
            if command == "await"     : self._await(line)        ;continue
            if command == "a"         : self._await(line)        ;continue
            if command == "write"     : self._write(line)        ;continue
            if command == "w"         : self._write(line)        ;continue
            if command == "enter"     : keyboard.press('enter')  ;continue
            if command == "."         : keyboard.press('enter')  ;continue
            if command == "scroll"    : self._scroll(line)       ;continue
            if command == "sl"        : self._scroll(line)       ;continue
            if command == "del"       : self._del(line)          ;continue
            if command == "d"         : self._del(line)          ;continue
            if command == "dd"        : self._del(line,'dir')    ;continue
            if command == "end"       : self._end()
            self._stopLoop()

        if self.autoswitch and self.switched == 1:
            time.sleep(self.autoswitch_pause)
            self._switch()

    # endregion

# region click arguments

CONTEXT_SETTINGS = dict(help_option_names=['-h','-help','--help'],max_content_width=400)

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-version', '-v', flag_value=True, default=False, help='show version number')
@click.option('--path', '-path', '-p', default='.', type=click.Path(dir_okay=True,file_okay=False,exists=True), help='set path of case, default: `.`')
@click.option('--clicklist', '-clicklist', '-c', default='t1.txt', type=click.STRING, help='set clicklist file of case, default:`t1.txt`')
@click.option('--images', '-images', '-i', default='images', type=click.STRING, help='set image directory of case, default: `images`')
@click.option('--confidence', '-confidence', '-co', default=0.95, type=click.FLOAT, help='set the accuracy of target detection - only values from 0.0 to 1.0 allowed, default: 0.95')
@click.option('--autoswitch','-autoswitch', '-a', flag_value=True, default=False, help='if set Clickomat will switch back to terminal after execution, default: False')
@click.option('--silent', '-silent', '-s', flag_value=True, default=False, help='if set Clickomat gives no terminal feedback, default: False')
@click.option('--step', '-step', '-st', default=0.06, type=click.FLOAT, help='set the pause length between each command, default: 0.06')
@click.option('--noswitch','-noswitch', '-n', flag_value=True, default=False, help='if set Clickomat will not execute switch commands unless they are marked with `!`')

def arguments(version,path,clicklist,images,confidence,autoswitch,silent,step,noswitch):

    """Clickomat documentation is available under https://github.com/skilleven/clickomat/wiki"""

    if version:
        print("Clickomat 0.3.0 is installed.\nYou may want to check if your version is up to date: pip list --outdated")
        exit()

    case_path = path

    # check if clicklist parameter is correct
    if not ".txt" in clicklist:
        input_file = f"{clicklist}.txt"
    input_file = os.path.join(case_path, clicklist)
    if not os.path.exists(input_file): 
        print(f"Specified clicklist is not existing: {input_file}")
        exit()

    # check if image folder parameter is correct
    if not images == ".":
        images_checkpath = os.path.join(case_path, images)
    else:
        images_checkpath = case_path
    if not os.path.exists(images_checkpath): 
        print(f"Specified image directory is not existing: {images_checkpath}")
        exit()

    if confidence > 1: 
        print("Confidence can have a maximum of 1.0!")
        exit()

    run(case_path,clicklist,images,confidence,autoswitch,silent,step,noswitch)
# endregion

#region Run
def run(case_path,input_file,images,confidence,autoswitch,silent,step,noswitch):
    c = Clickomat(case_path,input_file,images)

    c.confidence = confidence
    c.autoswitch = autoswitch
    c.step_pause = step
    if silent: c.logging = False
    if noswitch: c.switch = False

    c.main()
# endregion

if __name__ == "__main__":
    arguments()
