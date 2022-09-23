![Clickomat](https://repository-images.githubusercontent.com/538182878/848e85a0-25ec-49ee-8da3-37e597b04a89)

https://github.com/skilleven/clickomat/raw/main/clickomat-install.mp4

# Clickomat

Python-Script for automated click-sequences and text entry.

Building on top of the brilliant lib "pyautogui" by [Al Sweigart](https://github.com/asweigart)
it offers the possibility to perform mouse clicks, text input and more with very simplified commands.

The purpose of Clickomat is to map the sometimes relatively long python commands from pyautogui with short,
single-line commands that are processed in a simple text list.



## Commands
| Command | Result
|---|---
| **switch**                                | Alt-Tab on WIN / Command-Tab on Mac
| **click**                                 |  normal click at current position
| **click -_imagename_**                    |  click on imagename.png if present
| **click ! -_imagename_**                  |  forced click on imagename.png
| **doubleclick**                           |  normal doubleclick at current position
| **doubleclick -_imagename_**              |  doubleclick on imagename.png if present
| **doubleclick ! -_imagename_**            |  forced doubleclick on imagename.png
| **pos -_imagename_**                      |  place mouse on imagename.png
| **drag -_imagename_**                     |  click-drag across imagename.png (top/left to bottom/right)
| **drag up -_imagename_**                  |  click-drag across imagename.png (bottom/left to top/right)
| **await -_imagename_**                    |  waits for image to appear
| **write "text"**                          |  types text
| **enter**                                 |  press enter
| **scroll _20_**                           |  scroll 20 steps up
| **scroll _-20_**                          |  scroll 20 steps down
| **right _20_**                            |  pushes mouse 20px to the right
| **left _20_**                             |  pushes mouse 20px to the left
| **up _20_**                               |  pushes mouse 20px up
| **down _20_**                             |  pushes mouse 20px down
| **stop**                                  |  breaks the script (for debugging)
| **del**                                   |  deletes file
| **del dir**                               |  deletes directory
| **[number]**                              |  pauses for [number] seconds
| #                                         |  you can comment-out lines by using hash as first char

### Images:
-imagename can either be a single image or a list of images separated by '/'. The list will be iterated and the first finding will be used. See example in checkboxolympics testcase.


More commands coming...

---

## Dependencies:

```
* pyautogui
* keyboard
* easygui
```

### On some systems further dependencies may be needed/updated:

```
* opencv-python
* pillow
```

### Install on Windows:

```
$ pip install pyautogui keyboard easygui opencv-python pillow
```

### Install on Mac:

```
$ pip install pyautogui keyboard easygui
```

### Run Script:

cd into the testcases/checkboxolympics/ directory 
```
$ cd [path-to-clickomat-folder]/testcases/checkboxolympics
```
and run the script by typing

```
$ python c.py
```

---

## Examples:
- [examplescript.txt](https://github.com/skilleven/clickomat/blob/main/examplescript.txt)
- Testcase: checkboxolympics

On the Website https://checkboxolympics.com/ you can run the very simplyfied script of the testcase and get a score around 2.2 seconds...