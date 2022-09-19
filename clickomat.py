import pyautogui, re, time, keyboard
from datetime import datetime
import easygui as e

class Clickomat:

    input_file_name      = "t2.txt"
    confidence           = 0.97
    autoswitch           = False

    switched             = 0
    breakout             = False
    linenumber           = 0
    error                = ""

    def pause(self,line):
        try:
            pause = re.search(r"^[0-9]+$", line).group(0)
            time.sleep(int(pause))
        except:
            time.sleep(0.1)

    def getImage(self,line):
        try:
            image = re.search(r" -[a-zA-Z0-9_-]+", line).group(0)
            image = image[2:len(image)]
            image = f"{image}.png"
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
            x, y = pyautogui.locateCenterOnScreen(image, confidence = self.confidence)
            return True
        except:
            return False

    def locateImage(self,image):
        try:
            box = pyautogui.locateOnScreen(image, confidence = self.confidence)
            return box
        except:
            return False

    def clickImage(self,image):
        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence = self.confidence)
            pyautogui.click(x, y)
            return True
        except:
            return False

    def switch(self):
        pyautogui.keyDown('command')
        pyautogui.press('tab')
        pyautogui.keyUp('command')
        time.sleep(0.5)

    def write(self,line):
        try:
            text = re.search(r" \"[a-zA-Z0-9_\-\.\/]+\"", line).group(0)
            text = text[2:len(text)-1]
            print(" -> ", text, end = "")
            keyboard.write(text)
            return True
        except:
            print(" -> not written.", end = "")
            self.error = "Text could not be written"
            self.breakout = True
            return False

    def main(self):

        with open(self.input_file_name, 'r', encoding='UTF-8') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

        pyautogui.PAUSE = 0
        print("\n\n\n\n\n---------------------------------------------------")

        for line in lines:

            if self.breakout:
                print ("Loop broken!")
                e.msgbox("An error has occured: " + self.error, self.error)
                break

            self.linenumber += 1
            print(self.linenumber, end = " " )

            print(line, end = "" )
            self.pause(line)

            order = line.split(" ")

            if "switch" in order:
                self.switch()
                self.switched += 1

            if "click" in order:
                image = self.getImage(line)
                if not image: break
                if not self.clickImage(image):
                    print(" -> not clicked!", end="")
                    if "!" in order:
                        print()
                        self.error = "Forced image-click could not be executed"
                        print("Loop Broke!")
                        self.breakout = True
                        break
                else:
                    print(" -> clicked!", end="")

            if "pos" in order:
                image = self.getImage(line)
                if not image: break
                box = self.locateImage(image)
                if box:
                    print(" -> ", box, end = "")
                    pyautogui.moveTo((box[0]+(box[2]/2)),(box[1]+(box[3]/2)))
                else:
                    print(" -> Position not found!", end="")
                    self.error = "Position not found!"
                    self.breakout = True

            if "drag" in order:
                image = self.getImage(line)
                if not image: break
                box = self.locateImage(image)
                if box:
                    print(" -> ", box, end = "")

                    if "up" in order:
                        pyautogui.moveTo((box[0]),(box[1]+box[3]))
                        pyautogui.dragTo((box[0]+box[2]),(box[1]), button='left')
                    else:
                        pyautogui.moveTo(box[0],box[1])
                        pyautogui.dragTo((box[0]+box[2]),(box[1]+box[3]), button='left')
                else:
                    print(" -> nothing to drag!", end="")
                    self.error = "Nothing to drag!"
                    self.breakout = True

            if "wait" in order:

                found = False
                timeout = self.getTimeout(line)
                print(" -> timeout: " + str(timeout) + "s", end = "")
                start_time = datetime.now()

                while 1:
                    time_delta = datetime.now() - start_time
                    if time_delta.total_seconds() >= timeout:
                        break

                    image = self.getImage(line)
                    if self.findImage(image):
                        t=round(time_delta.total_seconds())
                        print(" -> found after " + str(t) + "s.",end = "")
                        found = True
                        break

                if not found:
                    print(" -> Not found.", end = "")
                    error = "Image to wait for was not found."
                    breakout = True

            if "write" in order:
                self.write(line)

            if "enter" in order:
                keyboard.press('enter')

            if "scroll" in order:
                self.scroll(line)

            print()

        if self.autoswitch and self.switched == 1:
            self.switch()

        if not self.breakout:
            print()
            print ("Loop finished.")

if __name__ == "__main__":
    c = Clickomat()
    c.main()