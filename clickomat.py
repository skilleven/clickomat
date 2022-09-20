import pyautogui, re, time, keyboard, os
from datetime import datetime
from os.path import exists
import easygui as e

class Clickomat:

    def __init__(self, case_path=None, input_file_name=None, images=None):

        if case_path is None:
            self.case_path = "."
        else:
            self.case_path = case_path
            if not os.path.isdir(self.case_path):
                print("given case path is not existing.")
                exit()

        if input_file_name is None:
            self.input_file_name = "t1.txt"
        else:
            self.input_file_name = input_file_name
            if not exists( self.input_file_name):
                print("given clicklist is not existing.")
                exit()

        if images is None:
            self.images = "."
        else:
            self.images = images
            if not os.path.isdir(self.images):
                print("given case path is not existing.")
                exit()

        self.input_file_path      = f"{self.case_path}/{self.input_file_name}"
        self.confidence           = 0.98
        self.autoswitch           = False

        self.logging              = False
        self.step_pause_min       = 0.03
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
            if self.step_pause_min > 0:
                time.sleep(self.step_pause_min)

    def getImage(self,line):

        image = False
        try: image = re.search(r" -[a-zA-Z0-9_-]+", line).group(0)
        except: pass
        if not image: return "Click"

        try:
            image = re.search(r" -[a-zA-Z0-9_-]+", line).group(0)
            image = image[2:len(image)]
            image = f"{self.images}/{image}.png"

            if not exists(image):
                return False

            return image

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
        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence=self.confidence)
            return True
        except:
            return False

    def locateImage(self,image):
        try:
            box = pyautogui.locateOnScreen(image, confidence=self.confidence)
            return box
        except:
            return False

    def clickImage(self,image):
        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence=self.confidence)
            pyautogui.click(x, y)
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

    def file(self,line):
        try:
            file = re.search(r" \"[a-zA-Z0-9_:\-\.\/\\]+\"", line).group(0)
            file = file[2:len(file)-1]
            return file
        except:
            return False

    def stop(self):
        self.stopped = True

    def image_not_found(self):
        self.error = "Target image not existing!"
        if self.logging: print(" -> Target image not existing! Check directory for screenshot-snippet.")
        self.breakout = True

    def right(self,line):
        amount = re.search(r" [0-9]+", line).group(0)
        amount = int(amount)
        pyautogui.moveRel(amount, 0)

    def main(self):

        with open(self.input_file_path, 'r', encoding='UTF-8') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

        pyautogui.PAUSE = 0
        if self.logging: print("\n\n\n\n\n---------------------------------------------------")

        for line in lines:

            if self.breakout:
                if self.logging: print ("Loop broken!\n\n")
                e.msgbox("An error has occured: " + self.error, self.error)
                break
            if self.stopped:
                if self.logging: print ("Loop stopped!\n\n")
                break

            self.linenumber += 1
            if self.logging: print(self.linenumber, end = " " )

            if self.logging: print(line, end = "" )
            self.pause(line)

            order = line.split(" ")

            if "stop" in order:
                self.stop()

            if "switch" in order:
                self.switch()
                self.switched += 1

            if "right" in order:
                self.right(line)

            if "click" in order:
                image = self.getImage(line)

                if image == "Click":
                    pyautogui.click()
                    if self.logging: print(" -> clicked!", end="")

                else:

                    if not image:
                        self.image_not_found()
                        if self.logging: print("Loop Broke!\n\n")
                        self.breakout = True
                        break

                    if not self.clickImage(image):
                        if self.logging: print(" -> not clicked!", end="")
                        if "!" in order:
                            if self.logging: print()
                            self.error = "Forced image-click could not be executed"
                            if self.logging: print("Loop Broke!\n\n")
                            self.breakout = True
                            break
                    else:
                        if self.logging: print(" -> clicked!", end="")

            if "pos" in order:
                image = self.getImage(line)

                if not image:
                    self.image_not_found()
                    break

                box = self.locateImage(image)
                if box:
                    if self.logging: print(" -> ", box, end = "")
                    pyautogui.moveTo((box[0]+(box[2]/2)),(box[1]+(box[3]/2)))
                else:
                    if self.logging: print(" -> Position not found!", end="")
                    self.error = "Position not found!"
                    self.breakout = True

            if "drag" in order:
                image = self.getImage(line)

                if not image:
                    self.image_not_found()
                    break
                
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

            if "await" in order:

                found = False
                timeout = self.getTimeout(line)
                if self.logging: print(" -> timeout: " + str(timeout) + "s", end = "")
                start_time = datetime.now()

                image = self.getImage(line)

                if not image:
                    self.image_not_found()
                else:
                    if self.logging: print(" " + image)

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

            if "write" in order:
                self.write(line)

            if "enter" in order:
                keyboard.press('enter')

            if "scroll" in order:
                self.scroll(line)

            if "del" in order:
                file = self.file(line)
                try:
                    os.remove(file)
                except:
                    pass


            if self.logging: print()

        if self.autoswitch and self.switched == 1:
            self.switch()

        if not self.breakout:
            if self.logging: print()
            if self.logging: print ("Loop finished.\n\n")

if __name__ == "__main__":

    c = Clickomat()
    c.main()