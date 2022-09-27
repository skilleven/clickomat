![Clickomat](https://repository-images.githubusercontent.com/538182878/848e85a0-25ec-49ee-8da3-37e597b04a89)

# Clickomat

Python-Script for automated click-sequences and text entry.

Building on top of the brilliant lib "pyautogui" by [Al Sweigart](https://github.com/asweigart)
it offers the possibility to perform mouse clicks, text input and more with very simplified commands.

The purpose of Clickomat is to map the sometimes relatively long python commands from pyautogui with short,
single-line commands that are processed in a simple text list.

## Installation 
[https://img.shields.io/badge/PyPI%20package-0.1.3-brightgreen?style=for-the-badge&logo=Pypi&logoColor=white](https://pypi.org/project/clickomat/)




```
pip install clickomat
```

### Run Testscript:

Open https://checkboxolympics.com/ in Firefox (Chrome should work also). \
It must now be ensured that ALT-TAB (Win) or CMD-TAB (Mac) can be used to switch directly back and forth between the terminal and the website.

Change directory into testcases/checkboxolympics/ 
```
cd [path-to-clickomat-folder]/testcases/checkboxolympics
```
and run the script by typing

```
python c.py
```


## Commands
| Command | Result
|---|---
| **switch**                                | Alt-Tab on WIN / Command-Tab on Mac
| **click**                                 |  normal click at current position
| **click -_images_**                       |  click on imagename.png if present
| **click ! -_images_**                     |  forced click on imagename.png
| **doubleclick**                           |  normal doubleclick at current position
| **doubleclick -_images_**                 |  doubleclick on imagename.png if present
| **doubleclick ! -_images_**               |  forced doubleclick on imagename.png
| **pos -image**                            |  place mouse on imagename.png
| **drag -image**                           |  click-drag across imagename.png (top/left to bottom/right)
| **drag up -image**                        |  click-drag across imagename.png (bottom/left to top/right)
| **await -_images_**                       |  waits for image to appear
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
| **lookup -image script.py**               |  set a target to lookout for the entire runtime. If found start script.

### Images:
-imagename can either be a single image or a list of images separated by '/'. The list will be iterated and the first finding will be used. See example in checkboxolympics testcase.


More commands coming...

[Documentation](https://github.com/skilleven/clickomat/wiki) is under construction.

---

## Dependencies:

```
* pyautogui
* keyboard
* easygui
* opencv-python (on windows pyautogui works only with opencv)
* pillow (on windows pyautogui works only with pillow)
```


---

## Examples:
- [examplescript.txt](https://github.com/skilleven/clickomat/blob/main/examplescript.txt)
- Testcase: checkboxolympics

On the Website https://checkboxolympics.com/ you can run the very simplyfied script of the testcase and get a score around 2.2 seconds...
