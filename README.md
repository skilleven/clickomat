# Clickomat

Python-Script for automated click-sequences and text entry.

## Commands
| Command | Result
|---|---
| **switch** | Alt-Tab on WIN / Command-Tab on Mac
| **click**  |  normal click at current position
| **click -imagename**  |  click on imagename.png if present
| **click ! -imagename**  |  forced click on imagename.png
| **pos -imagename**  |  place mouse on imagename.png
| **drag -imagename**  |  click-drag across imagename.png (top/left to bottom/right)
| **drag up -imagename**  |  click-drag across imagename.png (bottom/left to top/right)
| **await -imagename**  |  waits for image to appear
| **write "text"**  |  types text
| **enter**  |  presses enter
| **scroll 20**  |  scroll 20 steps up
| **scroll -20**  |  scroll 20 steps down
| **stop**  |  breaks the script (for debugging)
| **del**  |  deletes file
| **[number]**  |  pauses for [number] seconds


---

### Dependencies:

* pyautogui
* keyboard
* easygui

### On some systems further dependencies may be needed/updated:

* opencv-python
* pillow