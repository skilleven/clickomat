import pyautogui, re, time, keyboard, os, shutil # type: ignore
import easygui as easygui # type: ignore
from datetime import datetime
from os.path import exists

class Clickomat:

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

        self.confidence           = 0.98
        self.autoswitch           = False
        self.autoswitch_pause     = 1

        self.logging              = False
        self.step_pause           = 0.1
        self.switch_pause         = 0
        self.switched             = 0
        self.breakout             = False
        self.stopped              = False
        self.linenumber           = 0
        self.error                = ""

    def pause(self,line):
        try:
            pause = re.search(r"^[0-9]+$", line).group(0)
            time.sleep(int(pause))
        except:
            if self.step_pause > 0:
                time.sleep(self.step_pause)

    def getImage(self,line):
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

    def scroll(self,line):
        try:
            amount = re.search(r" -?[0-9]+", line).group(0)
            amount = amount[1:len(amount)]
            amount = int(amount)
            pyautogui.scroll(amount)
            return True
        except:
            return False

    def getTimeout(self,line):
        try:
            timeout = re.search(r" [0-9]+ ", line).group(0)
            return int(timeout)
        except:
            return 10

    def findImage(self,image):
        x = False
        for i in image:
            try:
                x, y = pyautogui.locateCenterOnScreen(i, confidence=self.confidence)
            except: pass
            if x: return i
        return False

    def locateImage(self,image):
        try:
            box = pyautogui.locateOnScreen(image, confidence=self.confidence)
            return box
        except:
            return False

    def clickImage(self,image,mode):
        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence=self.confidence)
            if mode == 1: pyautogui.click(x, y)
            if mode == 2: pyautogui.doubleClick(x, y)
            return True
        except:
            return False

    def switch(self):
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

    def write(self,line):
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

    def getPath(self,line):
        try:
            path = re.search(r" \"[a-zA-Z0-9_:\-\.\/\\]+\"", line).group(0)
            path = path[2:len(path)-1]
            return path
        except:
            return False

    def stop(self):
        self.stopped = True

    def image_not_found(self):
        self.error = "Target image not existing!"
        if self.logging: print(" -> Target image not existing! Check directory for screenshot-snippet.")

    def push(self,order):
        amount = int(order[1])
        if order[0] == "up":    pyautogui.moveRel(0,amount*-1)
        if order[0] == "down":  pyautogui.moveRel(0,amount)
        if order[0] == "right": pyautogui.moveRel(amount,0)
        if order[0] == "left":  pyautogui.moveRel(amount*-1,0)

    def click(self,line,mode):
            image = self.getImage(line)
            if image != "Click":
                image = self.findImage(image)

            if image == "Click":
                pyautogui.click()
                if self.logging:
                    print(" -> clicked!", end="") if mode==1 else print(" -> doubleclicked!", end="")
            else:
                if not image:
                    self.image_not_found()

                if not self.clickImage(image,mode):
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
                        print(" -> clicked!", end="") if mode==1 else print(" -> doubleclicked!", end="")

    def pos(self,line):
                image = self.getImage(line)[0]
                if not image:
                    self.image_not_found()
                    return
                box = self.locateImage(image)
                if box:
                    if self.logging: print(" -> ", box, end = "")
                    pyautogui.moveTo((box[0]+(box[2]/2)),(box[1]+(box[3]/2)))
                else:
                    if self.logging: print(" -> Position not found!", end="")
                    self.error = "Position not found!"
                    self.breakout = True

    def drag(self,line):
        order = line.split(" ")
        image = self.getImage(line)[0]
        if not image:
            self.image_not_found()
            return
        box = self.locateImage(image)
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


    def _await(self,line):
        found = False
        timeout = self.getTimeout(line)
        if self.logging: print(" -> timeout: " + str(timeout) + "s", end = "")
        start_time = datetime.now()

        image = self.getImage(line)

        if not image:
            self.image_not_found()
        else:
            if self.logging: print(" " + str(image))

            while 1:
                time_delta = datetime.now() - start_time
                if time_delta.total_seconds() >= timeout:
                    break

                if self.findImage(image):
                    t=round(time_delta.total_seconds())
                    if self.logging: print(" -> found after " + str(t) + "s.",end = "")
                    found = True
                    break

            if not found:
                if self.logging: print(" -> Not found.", end = "")
                self.error = "Image to wait for was not found."
                self.breakout = True

    def _del(self,line):
        order = line.split(" ")

        path = self.getPath(line)
        if not path: return
        if "dir" in order:
            try:
                shutil.rmtree(path)
            except OSError as e:
                print(e)
            else:
                print("The directory is deleted successfully", end = "")
        else:
            try:
                os.remove(path)
            except OSError as e:
                print(e)
            else:
                print("The File is deleted successfully", end = "")

    def stopLoop(self):
        if self.breakout:
            if self.logging: print ("Loop broken!\n\n")
            easygui.msgbox("An error has occured: " + self.error, self.error)
            return
        if self.stopped:
            if self.logging: print ("Loop stopped!\n\n")
            return




    def main(self):

        if self.commands is not None:
            lines = iter(self.commands.splitlines())
        else:
            with open(self.input_file, 'r', encoding='UTF-8') as file:
                lines = file.readlines()

        lines = [line.rstrip() for line in lines]

        pyautogui.PAUSE = 0
        if self.logging: print("\n\n\n\n\n---------------------------------------------------")

        for line in lines:

            self.stopLoop()

            self.linenumber += 1
            if self.logging: print(self.linenumber, end = " " )

            if self.logging: print(line, end = "" )
            self.pause(line)

            order = line.split(" ")

            if order[0] == "#": continue

            if "stop" in order: self.stop()

            if "switch" in order:
                self.switch()
                self.switched += 1

            if "right" in order or "left" in order or "up" in order or "down" in order: self.push(order)

            if "click" in order or "doubleclick" in order:
                if "click" in order:       mode = 1
                if "doubleclick" in order: mode = 2
                self.click(line,mode)

            if "pos" in order: self.pos(line)

            if "drag" in order: self.drag(line)

            if "await" in order: self._await(line)

            if "write" in order: self.write(line)

            if "enter" in order: keyboard.press('enter')

            if "scroll" in order: self.scroll(line)

            if "del" in order: self._del(line)

            if self.logging: print()

        if self.autoswitch and self.switched == 1:
            time.sleep(self.autoswitch_pause)
            self.switch()

        if not self.breakout:
            if self.logging: print()
            if self.logging: print ("Loop finished.\n\n")

if __name__ == "__main__":

    c = Clickomat()
    c.main()