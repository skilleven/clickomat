import pyautogui, re, time, keyboard, os, shutil, click, threading # type: ignore
from tkinter import *
import tkinter.messagebox as tkmb
from datetime import datetime
from os.path import exists
from datetime import datetime
if os.name == 'nt': import msvcrt

#-----------------------------------------------------
#
# Clickomat v0.3.3
#
#-----------------------------------------------------

# region Watcher
class Watcher(threading.Thread):

    def __init__(self,parent,target,name="lookup"):
        threading.Thread.__init__(self)

        self._target      = target
        self._stop_event = threading.Event()
        self.parent      = parent
        self.name        = name

    def check(self):

        if self.name == "lookup" or self.name == "blacklist":
            if len(self._target):
                # _target comes in as list
                # _target[0]: list of images
                # _target[1]: target section
                if self.parent._findImage(self._target[0]):
                    return self.jumpSection()

        if self.name == "whitelist":
            if len(self._target):
                if not self.parent._findImage(self._target[0]):
                    return self.jumpSection()

        # print(f"\nWatcher empty: {self.name}")

    def jumpSection(self) -> None:
        self.parent.section = self._target[1]
        if self.parent.logging: print(f"\nImage lookup found -> Go Section {self.parent.section}!\n")
        self.parent.ClickLoop(self.parent.section)
        self.stop()

    def nullTarget(self):
        self._target = []

    def setTarget(self,target):
        self._target = target

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            # print(f"Watcher-Loop: {self.name} -> {str(self._target[1])}")
            self.check()
        # print(f"\nWatcher stopped: {self.name}")
# endregion


class Clickomat:
    # region __init__
    def __init__(self, case_path=None, input_file=None, images=None):
        # If ran from Python we grab the params here
        # self.commands is used if a multiline string is given instead a clicklist filename
        self.commands = None
        # case_path is the path to the root of the click-project
        # this is where the clicklist file and the image target folder is located under
        # default is the path of the calling python script (.)
        if case_path is None:
            self.case_path = "."
        else:
            self.case_path = case_path
            # we check if the path is even existing
            # if not -> abort
            if not os.path.isdir(self.case_path):
                print(self.case_path)
                print("given case path is not existing.")
                exit()

        if input_file is None:
            # input_file is the name of the clicklist - not the path
            # default is "t1.txt"
            self.input_file = "t1.txt"
        else:
            self.input_file = input_file
            if ".txt" not in self.input_file:
                # this means there was not a txt file specified
                # but an actual list (lines) of commands
                self.commands = self.input_file
            else:
                # we also test the existence of the text file
                # if not present -> abort
                self.input_file = f"{self.case_path}/{self.input_file}"
                if not exists(self.input_file):
                    print(self.input_file)
                    print("given clicklist is not existing.")
                    exit()

        # images contains the name of the folder where the targets (PNGs) are stored
        if images is None:
            self.images = "."
        else:
            # ... and of course we check for existence
            self.images = f"{self.case_path}/{images}"
            if not os.path.isdir(self.images):
                print(self.input_file)
                print("given image location is not existing.")
                exit()

        # Default Parameters
        self.confidence           = 0.95
        self.autoswitch           = False
        self.autoswitch_pause     = 1

        self.logging              = True
        self.step_pause           = 0.06
        self.switch_pause         = 0
        self.switched             = 0
        self.switch               = True

        # Flags
        self.breakout             = False
        self.stopped              = False
        self.error                = ""
        self.test                 = False # needed for pytest

    # endregion
    # region _pause(line)
    def _pause(self,line):
        # pause method is run before every command
        # this method is only checking if the current command line contains a pause command
        # if yes the amount of that pause is returned
        # if not the default step pause is returned IF it is >0
        # when False is returned the actual pause in the clickloop is skipped
        def sp():
            if self.step_pause > 0:
                return float(self.step_pause)
            else:
                return False
        if line == ".": sp()
        pause = re.search(r"^[0-9]+(\.?[0-9]+)?$", line)
        if pause:
            pause = pause.group(0)
            return float(pause)
        else:
            return sp()

    # endregion
    # region _getImage(line)
    def _getImage(self,line):
        # looks if 1 or more images can be found in the command line
        # and returns a list with png images
        # if no image(s) found 'Click' is returned and that causes the
        # click method to just click whereever the mause is located

        needle = " -([a-zA-Z0-9_/]-?)+"
        img = False
        result = []
        try: img = re.search(needle, line).group(0)
        except: return "Click"

        try:
            # if images pass the grep above
            # they are checked for existence here
            # if they can't be found False is returned
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
        # commands if, go and lookup are using target sections
        # this gives back such a section if the line contains either:
        # ->SECTION
        # -> SECTION
        # ->##SECTION
        # ->#SECTION
        # ...

        # sort out potential syntax errors
        line = line.replace("#","")

        needle = r"-> ?[a-zA-Z0-9_\-]+"
        section = False
        try:
            section = re.search(needle, line).group(0)
        except:
            print("no section found")
            return False
        try:
            section = re.search(needle, line).group(0)

            # sort out potential syntax errors
            section = section.replace(" ","")

            #         cut off the ->
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
            if not self.test: pyautogui.scroll(amount)
            return True
        except:
            return False
    # endregion
    # region _getTimeout(line)
    def _getTimeout(self,line,default=10):
        try:
            timeout = re.search(r" [0-9]+ ", line).group(0)
            return int(timeout)
        except:
            return default
    # endregion
    # region _findImage(image)
    def _findImage(self,image):
        # takes LIST of images!
        x = False
        for i in image:
            try:
                x,_ = pyautogui.locateCenterOnScreen(i, confidence=self.confidence)
            except: pass
            if x:
                return i
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
            x,y = pyautogui.locateCenterOnScreen(image, confidence=self.confidence)
            if mode == 1 and not self.test: pyautogui.click(x, y)
            if mode == 2 and not self.test: pyautogui.doubleClick(x, y)
            if mode == 3 and not self.test: self._shiftclick(x, y)
            return True
        except:
            return False
    # endregion
    # region _switch()
    def _switch(self):
    # no unittest for this
        if os.name == 'nt':
            if not self.test: pyautogui.keyDown('alt')
            if not self.test: pyautogui.press('tab')
            if not self.test: pyautogui.keyUp('alt')
        else:
            if not self.test: pyautogui.keyDown('command')
            if not self.test: pyautogui.press('tab')
            if not self.test: pyautogui.keyUp('command')
        if self.switch_pause > 0:
            time.sleep(self.switch_pause)
    # endregion
    # region _write(line)
    def _write(self,line):
        try:
            # text = re.search(r" \"[a-zA-Z0-9_:@\-\.\/\\ ]+\"", line).group(0)
            text = re.search(r" \".+\"", line).group(0)
            text = text[2:len(text)-1]
            if self.logging: print(" -> ", text, end = "")
            if not self.test: keyboard.write(text)
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
        if order[0] == "up":
            if not self.test: pyautogui.moveRel(0,amount*-1)
            return 'up'
        if order[0] == "down":
            if not self.test: pyautogui.moveRel(0,amount)
            return 'down'
        if order[0] == "right":
            if not self.test: pyautogui.moveRel(amount,0)
            return 'right'
        if order[0] == "left":
            if not self.test: pyautogui.moveRel(amount*-1,0)
            return 'left'
        return False
    # endregion
    # region _click(line,mode)
    def _click(self,line,mode):
            image = self._getImage(line)

            if not image:
                self._imageNotFound()
                return("imageNotFound")

            if image != "Click":
                image = self._findImage(image)

            if image == "Click":
                if mode==1:
                    if not self.test: pyautogui.click()
                    if self.logging: print(" -> clicked!", end="")
                    return("normalClickExecuted")

                if mode==2:
                    if not self.test: pyautogui.doubleclick()
                    if self.logging: print(" -> doubleclicked!", end="")
                    return("normalDoubleClickExecuted")

                if mode==3:
                    if not self.test: self._shiftclick()
                    if self.logging: print(" -> shift-clicked!", end="")
                    return("normalShiftClickExecuted")

            if not self._clickImage(image,mode):
                if self.logging: print(" -> not clicked!", end="")
                order = line.split(" ")
                if " ! " in order:
                    if self.logging: print()
                    self.error = "Forced image-click could not be executed"
                    if self.logging: print("Loop Broke!\n\n")
                    self.breakout = True
                    return ("Forced_ImgClick_could_not_be_executed")
                else:
                    return ("ImgClick_could_not_be_executed")

            if mode==1:
                if self.logging: print(" -> clicked!", end="")
                return ("ImgClick_ClickExecuted")
            if mode==2:
                if self.logging: print(" -> doubleclicked!", end="")
                return ("ImgClick_DoubleClickExecuted")
            if mode==3:
                if self.logging: print(" -> shift-clicked!", end="")
                return ("ImgClick_ShiftClickExecuted")
    # endregion
    # region _pos(line)
    def _pos(self,line):
        image = self._getImage(line)
        try: image = image[0]
        except: pass

        if not image:
            self._imageNotFound()
            return("imageNotFound")

        box = self._locateImage(image)
        if box:
            if self.logging: print(" -> ", box, end = "")
            if not self.test: pyautogui.moveTo((box[0]+(box[2]/2)),(box[1]+(box[3]/2)))
            return("positionedSuccessful")
        else:
            if self.logging: print(" -> Position not found!", end="")
            self.error = "Position not found!"
            self.breakout = True
            return("positionFail")
    # endregion
    # region _posxy(line)
    def _posxy(self,line,mode):
        needle = r" [0-9]+"
        if not self.test: x, y = pyautogui.position()
        try:
            amount = int(re.search(needle, line).group(0)[1:])
            if mode == 'y': y = amount
            if mode == 'x': x = amount
        except:
            print("no value assigned!")
            return False
        try:
            if not self.test: pyautogui.moveTo(x,y)
            return True
        except:
            return False
    # endregion
    # region _mDownUp(line)
    def _mDownUp(self,line):
        if line == "mdown" or line == "md":
            if not self.test: pyautogui.mouseDown()
            return "mdown"
        if line == "mup" or line == "mu":
            if not self.test: pyautogui.mouseUp()
            return "mup"
    # endregion
    # region _drag(line)
    def _drag(self,line):
        # TODO: strange behavior with set duration
        order = line.split(" ")
        image = self._getImage(line)
        dur   = self._getTimeout(line,1)
        try: image = image[0]
        except: pass
        if not image:
            self._imageNotFound()
            return("imageNotFound")

        box = self._locateImage(image)
        if box:
            if self.logging: print(" -> ", box, end = "")
            if "up" in order:
                if not self.test: pyautogui.moveTo((box[0]),(box[1]+box[3]))
                if not self.test: pyautogui.dragTo((box[0]+box[2]),(box[1]), button='left')
                if not self.test and dur: pyautogui.dragTo((box[0]+box[2]),(box[1]), dur , button='left')
                return ("dragUpSuccess")
            else:
                if not self.test: pyautogui.moveTo(box[0],box[1])
                if not self.test: pyautogui.dragTo((box[0]+box[2]),(box[1]+box[3]), button='left')
                if not self.test and dur: pyautogui.dragTo((box[0]+box[2]),(box[1]+box[3]), dur , button='left')
                return ("dragSuccess")
        else:
            if self.logging: print(" -> nothing to drag!", end="")
            self.error = "Nothing to drag!"
            self.breakout = True
            return ("nothingToDrag")
    # endregion
    # region _await(line)
    def _await(self,line):
        found = False
        timeout = self._getTimeout(line)
        if self.test and timeout > 3: timeout = 2
        if self.logging: print(" -> timeout: " + str(timeout) + "s", end = "")
        start_time = datetime.now()

        image = self._getImage(line)
        if not image:
            self._imageNotFound()
            return("imageNotFound")

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
            return ("imageNotFound")

        return ("imageFound")
    # endregion
    # region _del(line)
    def _del(self,line,mode="file"):

        order = line.split(" ")
        path  = self._getPath(line)
        if not path: return ("noPath")

        if "dir" in order: mode = "dir"

        if mode == "file":
            try:
                os.remove(path)
            except OSError as e:
                print(e)
                return("delFail")
            else:
                if self.logging: print("The File is deleted successfully", end = "")
                return("delSuccess")

        if mode == "dir":
            try:
                shutil.rmtree(path)
            except OSError as e:
                print(e)
            else:
                if self.logging: print("The directory is deleted successfully", end = "")
                return("delDirSuccess")
    # endregion
    # region _stopLoop()
    def _stopLoop(self):
        self._abort()
        if self.breakout and not self.test:
            if self.logging: print ("Loop broken!\n\n")
            message = "An error has occured: " + self.error
            self._popupMessage(message,'error')
            try: self.Lookup.stop()
            except: pass
            exit()

        if self.stopped:
            if self.logging: print ("Loop stopped!\n\n")
            try: self.Lookup.stop()
            except: pass
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
        image = self._getImage(line)
        sec   = self._getSection(line)

        if image and sec: target = [image,sec]
        if self.logging: print(target)

        try:
            self.Lookup.setTarget(target)
        except:
            self.Lookup = Watcher(self,target)
            self.Lookup.start()

        # if self.logging:
        #     print("\nWatcher Started- target:")
        #     print(target)
        #     print("\n")
        return
    # endregion
    # region _if(line)
    def _if(self,line):
        image = self._getImage(line)
        sec = self._getSection(line)
        if self._findImage(image) and sec:
            if self.logging: print(f"\nImage (if) found -> Go Section {sec}!\n")
            self.section = sec
            if not self.test: self.ClickLoop(self.section)
            return ("success")
        return ("fail")
    # endregion
    # region _go(line)
    def _go(self,line):
        sec = self._getSection(line)
        if sec:
            if self.logging: print(f"\nGo Section {sec}!\n")
            self.section = sec
            if not self.test: self.ClickLoop(self.section)
            return ("success")
        return ("fail")
    # endregion
    # region _abort()
    def _abort(self):
        try:
            if msvcrt.kbhit() and msvcrt.getch().decode() == chr(27):
                self.Lookup.stop()
                exit()
        except:
            pass
    # endregion
    # region _popupMessage(message,t='info') t -> type
    def _popupMessage(self,message,typ='info',title='Clickomat'):
        if typ == "info":    tkmb.showinfo(title=title, message=message)
        if typ == "error":   tkmb.showerror(title=title, message=message)
        if typ == "warning": tkmb.showwarning(title=title, message=message)
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
        if not self.test: pyautogui.screenshot(filename)
    # endregion
    # region _shiftclick(x,y)
    def _shiftclick(self,x=None,y=None):
        if not self.test: pyautogui.keyDown('shift')
        if not x and not y:
            if not self.test: pyautogui.click()
        else:
            if not self.test: pyautogui.click(x,y)
        if not self.test: pyautogui.keyUp('shift')
    #endregion
    # region _pop(line)
    def _pop(self,line):
        try:
            text = re.search(r" \".+\"", line).group(0)
            text = text[2:len(text)-1]
            if self.logging: print(" -> ", text, end = "")
            if not self.test: self._popupMessage(text,typ='info',title='User Message')
            return True
        except:
            self.error = "No text for popup found"
            self.breakout = True
            return False
    #endregion
    # region _routes(command)
    def _routes(self,command):
        if command == "screenshot": return("self._screenshot()")
        if command == "shot"      : return("self._screenshot()")
        if command == "drag"      : return("self._drag(line)")
        if command == "mdown"     : return("self._mDownUp(line)")
        if command == "md"        : return("self._mDownUp(line)")
        if command == "mup"       : return("self._mDownUp(line)")
        if command == "mu"        : return("self._mDownUp(line)")
        if command == "pos"       : return("self._pos(line)")
        if command == "posX"      : return("self._posxy(line,'x')")
        if command == "X"         : return("self._posxy(line,'x')")
        if command == "x"         : return("self._posxy(line,'x')")
        if command == "posY"      : return("self._posxy(line,'y')")
        if command == "Y"         : return("self._posxy(line,'y')")
        if command == "y"         : return("self._posxy(line,'y')")
        if command == "if"        : return("self._if(line)")
        if command == "go"        : return("self._go(line)")
        if command == "await"     : return("self._await(line)")
        if command == "a"         : return("self._await(line)")
        if command == "write"     : return("self._write(line)")
        if command == "w"         : return("self._write(line)")
        if command == "enter"     : return("keyboard.press('enter')")
        if command == "."         : return("keyboard.press('enter')")
        if command == "scroll"    : return("self._scroll(line)")
        if command == "sl"        : return("self._scroll(line)")
        if command == "del"       : return("self._del(line)")
        if command == "d"         : return("self._del(line)")
        if command == "dd"        : return("self._del(line,'dir')")
        if command == "pop"       : return("self._pop(line)")
        return False
    #endregion
    # region _clickRoute(command,line)
    def _clickRoute(self,command,line):
        if command=="click" \
        or command=="doubleclick" \
        or command=="shiftclick" \
        or command=="c" or command=="dc" or command=="sc":
            if command=="click" or command=="c"        : mode = 1
            if command=="doubleclick" or command=="dc" : mode = 2
            if command=="shiftclick" or command=="sc"  : mode = 3
            return(f"self._click('{line}',{mode})")
    #endregion
    # region _pushRoute(command,order)
    def _pushRoute(self,command,order):
        if (command=="right" or command=="left" or command=="up" or command=="down") \
        or (command=="r"     or command=="l"    or command=="u"  or command=="d")    :
            return(f"self._push({order})")
    #endregion
    # region _getClicklist()
    def _getClicklist(self):

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
    #endregion
    # region main()
    def main(self):

        if self.logging: print(f"Case Path: {self.case_path}")
        if self.logging: print(f"Clicklist: {self.input_file}")
        if self.logging: print(f"Image Directory: {self.images}")
        if self.logging: print("---")

        self._getClicklist()

        if not self.test: pyautogui.PAUSE = 0
        if self.logging: print("\n\n\n\n\n---------------------------------------------------")

        self.ClickLoop(self.section)

        if not self.breakout:
            if self.logging: print()
            if self.logging: print ("Loop finished.\n\n")
    # endregion
    # region clickloop

    def ClickLoop(self,sec):

        try: self.Lookup.nullTarget()
        except: pass

        if self.logging: print(f"Running section: {sec}")

        for line in self.sections[sec]:

            # TODO: section control as Watcher?
            if sec != self.section: break

            lnr  = line[0]
            line = line[1]

            if self.logging: print()

            p = self._pause(line)
            if p: time.sleep(p)

            # TODO: stoploop as Watcher?
            self._stopLoop()

            if self.logging: print(lnr, end = " " )
            if self.logging: print(line, end = "" )

            # Thre at...
            if sec != self.section: break

            order   = line.split(" ")
            command = order[0]

            if command == "#": continue

            # lookup is a Watcher now (>= v0.3.3)
            if command == "lookup" or command == "lu":
                self._setLookup(line)

            # Threat...
            if sec != self.section: break

            if command == "stop":
                self._stop()
                break

            if command == "switch" or command == ">":
                if self.switch or "!" in order:
                    self._switch()
                    self.switched += 1
                continue

            # Threat...
            if sec != self.section: break

            # Threat...
            self._stopLoop()

            pushroute = self._pushRoute(command,order)
            if pushroute: eval(pushroute); continue

            # Threat...
            self._stopLoop()

            clickroute = self._clickRoute(command,line)
            if clickroute: eval(clickroute); continue

            # Threat...
            self._stopLoop()

            route = self._routes(command)
            if route: eval(route); continue

            if command == "end": self._end()

            # Threat...
            self._stopLoop()

        self.Lookup.stop()

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
def run(version,path,clicklist,images,confidence,autoswitch,silent,step,noswitch):

    """Clickomat documentation is available under https://github.com/skilleven/clickomat/wiki"""

    if version:
        print("Clickomat 0.3.2 is installed.\nYou may want to check if your version is up to date: pip list --outdated")
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

    go(case_path,clicklist,images,confidence,autoswitch,silent,step,noswitch)
# endregion

#region go
def go(case_path,input_file,images,confidence,autoswitch,silent,step,noswitch):
    c = Clickomat(case_path,input_file,images)
    c.confidence = confidence
    c.autoswitch = autoswitch
    c.step_pause = step
    if silent: c.logging = False
    if noswitch: c.switch = False
    c.main()
# endregion

if __name__ == "__main__":
    run()
