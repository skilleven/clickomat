# Clickomat

Python-Script for automated click-sequences and text entry.

## Commands
| Command | Result
|---|---
| **switch**                | Alt-Tab on WIN / Command-Tab on Mac
| **click**                 |  normal click at current position
| **click -_imagename_**    |  click on imagename.png if present
| **click ! -_imagename_**  |  forced click on imagename.png
| **pos -_imagename_**      |  place mouse on imagename.png
| **drag -_imagename_**     |  click-drag across imagename.png (top/left to bottom/right)
| **drag up -_imagename_**  |  click-drag across imagename.png (bottom/left to top/right)
| **await -_imagename_**    |  waits for image to appear
| **write "text"**          |  types text
| **enter**                 |  press enter
| **scroll _20_**           |  scroll 20 steps up
| **scroll _-20_**          |  scroll 20 steps down
| **right _20_**            |  pushes mouse 20px to the right
| **stop**                  |  breaks the script (for debugging)
| **del**                   |  deletes file
| **[number]**              |  pauses for [number] seconds
| #                         |  you can comment-out lines by using hash (no space)

## Todo
| Command | Result
|---|---
| **doubleclick**                 |  normal doubleclick at current position
| **doubleclick -_imagename_**    |  doubleclick on imagename.png if present
| **doubleclick ! -_imagename_**  |  forced doubleclick on imagename.png
| **left _20_**                   |  pushes mouse 20px to the left
| **up _20_**                     |  pushes mouse 20px up
| **down _20_**                   |  pushes mouse 20px down
| ...  |  ...


---

### Dependencies:

* pyautogui
* keyboard
* easygui

### On some systems further dependencies may be needed/updated:

* opencv-python
* pillow

---

## Examples:
- [examplescript.txt](https://github.com/skilleven/clickomat/blob/main/examplescript.txt)
- Testcase: checkboxolympics

On the Website https://checkboxolympics.com/ you can run the very simplyfied script of the testcase and get a score around 2.2 seconds...