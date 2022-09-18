import pyautogui, re, time, keyboard
from datetime import datetime
import easygui as e

input_file_name      = "t2.txt"
confidence           = 0.97
autoswitch           = False

switched             = 0
breakout             = False
linenumber           = 0
error =""

def pause(line):
    try:
        pause = re.search(r"^[0-9]+$", line).group(0)
        time.sleep(int(pause))
    except:
        time.sleep(0.1)

def getImage(line):
    try:
        image = re.search(r" -[a-zA-Z0-9_-]+", line).group(0)
        image = image[2:len(image)]
        image = f"{image}.png"
        return image
    except:
        return False

def scroll(line):
    try:
        amount = re.search(r" -?[0-9]+", line).group(0)
        amount = amount[1:len(amount)]
        amount = int(amount)
        pyautogui.scroll(amount)
        return True
    except:
        return False

def getTimeout(line):
    try:
        timeout = re.search(r" [0-9]+ ", line).group(0)
        return int(timeout)
    except:
        return 10

def findImage(image):
    try:
        x, y = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        return True
    except:
        return False

def locateImage(image):
    try:
        box = pyautogui.locateOnScreen(image, confidence=confidence)
        return box
    except:
        return False

def clickImage(image):
    try:
        x, y = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        pyautogui.click(x, y)
        return True
    except:
        return False

def switch():
    pyautogui.keyDown('command')
    pyautogui.press('tab')
    pyautogui.keyUp('command')
    time.sleep(0.5)

def write(line):
    try:
        text = re.search(r" \"[a-zA-Z0-9_\-\.\/]+\"", line).group(0)
        text = text[2:len(text)-1]
        print(" -> ", text, end = "")
        keyboard.write(text)
        return True
    except:
        print(" -> not written.", end = "")
        error = "Text could not be written"
        breakout = True
        return False


with open(input_file_name, 'r', encoding='UTF-8') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

pyautogui.PAUSE = 0
print("\n\n\n\n\n---------------------------------------------------")

for line in lines:

    if breakout:
        print ("Loop broken!")
        e.msgbox("An error has occured: " + error, error)
        break

    linenumber += 1
    print(linenumber, end = " " )

    print(line, end = "" )
    pause(line)

    order = line.split(" ")

    if "switch" in order:
        switch()
        switched += 1

    if "click" in order:
        image = getImage(line)
        if not image: break
        if not clickImage(image):
            print(" -> not clicked!", end="")
            if "!" in order:
                print()
                error = "Forced image-click could not be executed"
                print("Loop Broke!")
                breakout = True
                break
        else:
            print(" -> clicked!", end="")

    if "pos" in order:
        image = getImage(line)
        if not image: break
        box = locateImage(image)
        if box:
            print(" -> ", box, end = "")
            pyautogui.moveTo((box[0]+(box[2]/2)),(box[1]+(box[3]/2)))
        else:
            print(" -> Position not found!", end="")
            error = "Position not found!"
            breakout = True

    if "drag" in order:
        image = getImage(line)
        if not image: break
        box = locateImage(image)
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
            error = "Nothing to drag!"
            breakout = True

    if "wait" in order:

        found = False
        timeout = getTimeout(line)
        print(" -> timeout: " + str(timeout) + "s", end = "")
        start_time = datetime.now()

        while 1:
            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() >= timeout:
                break

            image = getImage(line)
            if findImage(image):
                t=round(time_delta.total_seconds())
                print(" -> found after " + str(t) + "s.",end = "")
                found = True
                break

        if not found:
            print(" -> Not found.", end = "")
            error = "Image to wait for was not found."
            breakout = True

    if "write" in order:
        write(line)

    if "enter" in order:
        keyboard.press('enter')

    if "scroll" in order:
        scroll(line)

    print()

if autoswitch and switched == 1:
    switch()

if not breakout:
    print()
    print ("Loop finished.")
