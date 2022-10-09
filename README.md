![Clickomat](https://repository-images.githubusercontent.com/538182878/80262157-c719-4543-b85c-c77e26655a5f)



# Clickomat 1.0.4

Python-Script for automated click-sequences and text entry.

Building on top of the brilliant lib "pyautogui" by [Al Sweigart](https://github.com/asweigart)
it offers the possibility to perform mouse clicks, text input and more with very simplified commands.

The purpose of Clickomat is to map the sometimes relatively long python commands from pyautogui with short,
single-line commands that are processed in a simple text list.



<br><br>


## Installation
[![PyPI](https://img.shields.io/badge/PyPI%20package-1.0.4-brightgreen?style=for-the-badge&logo=Pypi&logoColor=white)](https://pypi.org/project/clickomat/)


```
$ pip install clickomat
```

Watch how easy it is to get started:

https://user-images.githubusercontent.com/11266793/194589489-784effbd-e261-4cf5-beb5-010c3b57e6a3.mp4


**FOR MAC USERS:**

Unfortunately, one of the used modules (tkinter) caused problems in previous versions.
If you have Monterey installed clickomat crashed with a long, cryptic exception.
I changend the module and v1.0.3 or higher is now working on mac again!

<br><br>


### Run Testscript

Open https://checkboxolympics.com/ in Firefox (other browsers render differently so targets are not recognized). \
It must now be ensured that ALT-TAB (Win) or CMD-TAB (Mac) can be used to switch directly back and forth between the terminal and the website.

1) Install Clickomat package
```
$ pip install clickomat
```
2) Change directory into testcases/checkboxolympics/
```
$ cd [path-to-clickomat-folder]/testcases/checkboxolympics
```
3) Run the script by typing

```
$ python c.py
```

OR simply put
```
$ pip install clickomat
...
$ clickomat -p [path-to-clickomat-folder]/testcases/checkboxolympics

```

<br><br>

### Run Clickomat


#### From command-line as CLI
If run directly from command-line Clickomat takes arguments like this:

```
$ clickomat -p C:/path/to/case/dir -c clicklist.txt -i imagefolder
```
Defaults would simply be '.','t1.txt','images' if called w/o arguments.

If you only like to change the clicklist-file:

```
$ clickomat -c clicklist.txt
```
More details in the [Docs -> CLI](https://github.com/skilleven/clickomat/wiki/CLI)

<br>

#### From python-file

To run from python-script you need to have at least this construct:
```python
from clickomat import Clickomat
c = Clickomat('.','t1.txt',"images")
c.main()
```
* You have to specify the location of your clicklist with the first param. Here it is a dot because the python file is in the same directory as the Clickomat script txt-file (clicklist).
* Next is the name of the clicklist (text-file) to read instructions from `t1.txt`
* You CAN specify a folder for your target-images but those can also be located on txt-file level. Then you would write a dot here.

More details in the [Docs -> Python](https://github.com/skilleven/clickomat/wiki/Python)


<br>

---

<br>

## Commands
| Command | Result
|---|---
| ##SECTION                                 |  you can divide your script into sections
| **switch**                                |  Alt-Tab on WIN / Command-Tab on Mac
| **click**                                 |  normal click at current position
| **click -_images_**                       |  click on imagename.png if present
| **click ! -_images_**                     |  forced click on imagename.png
| **doubleclick**                           |  normal doubleclick at current position
| **doubleclick -_images_**                 |  doubleclick on imagename.png if present
| **doubleclick ! -_images_**               |  forced doubleclick on imagename.png
| **shiftclick**                            |  shift-click at current position
| **shiftclick -_images_**                  |  shift-click on imagename.png if present
| **shiftclick ! -_images_**                |  forced shift-click on imagename.png
| **mdown**                                 |  Mouse-Down - Stays down until released by `mup` !
| **mup**                                   |  Mouse-Up
| **pos -image**                            |  place mouse on imagename.png
| **posX _20_**                             |  move mouses X-coordinate to 20px from left
| **posY _20_**                             |  move mouses Y-coordinate to 20px from top
| **right _20_**                            |  pushes mouse 20px to the right
| **left _20_**                             |  pushes mouse 20px to the left
| **up _20_**                               |  pushes mouse 20px up
| **down _20_**                             |  pushes mouse 20px down
| **drag -image**                           |  click-drag across imagename.png (top/left to bottom/right)
| **drag up -image**                        |  click-drag across imagename.png (bottom/left to top/right)
| **await -_images_**                       |  waits for image to appear
| **write "text"**                          |  types text
| **pop "text"**                            |  pops up a message, pauses until button is pressed
| **enter**                                 |  press enter
| **scroll _20_**                           |  scroll 20 steps up
| **scroll _-20_**                          |  scroll 20 steps down
| **stop**                                  |  breaks the script (for debugging)
| **del**                                   |  deletes file
| **del dir**                               |  deletes directory
| **[number]**                              |  pauses for [number] seconds
| #                                         |  you can comment-out lines by using hash as first char (followed by space)
| #command                                  |  you can also comment-out lines by using hash as first char followed by command (no space)
| **lookup -image ->SECTION**               |  set a target to lookout for the entire runtime. If found -> end current section, start SECTION (name)
| **if -_images_ ->SECTION**                |  If (multiple possible) target found -> end current section, start SECTION (name)
| **go ->SECTION**                          |  end current section, start SECTION (name)
| **end**                                   |  you CAN pop a message when script is finished - optional

### Images:
-imagename can either be a single image or a list of images separated by `/` . The list will be iterated and the first finding will be used. See example in [checkboxolympics testcase](https://github.com/skilleven/clickomat/tree/main/testcases/checkboxolympics).


## Shorthands
| Command | Shorthand | | Command | Shorthand | | Command | Shorthand
|-----|-----|-|------|------|-|------|------|
| **switch**      |  >   || **posX**  |  x   || **await**   |  a   |
| **click**       |  c   || **posY**  |  y   || **write**   |  w   |
| **doubleclick** |  dc  || **right** |  r   || **enter**   |  .   |
| **shiftclick**  |  sc  || **left**  |  l   || **scroll**  |  sl  |
| **mdown**       |  md  || **up**    |  u   || **del**     |  d   |
| **mup**         |  mu  || **down**  |  d   || **del dir** |  dd  |
|                 |      ||           |      || **lookup**  |  lu  |

More commands coming...

# [Full Documentation](https://github.com/skilleven/clickomat/wiki)

---

<br><br>

## Dependencies:

```
* pyautogui
* keyboard
* pynput
* click
* pyperclip
* opencv-python (on windows pyautogui works only with opencv)
* pillow (on windows pyautogui works only with pillow)
```

---

## Examples:
- [examplescript.txt](https://github.com/skilleven/clickomat/blob/main/examplescript.txt)
- Testcase: [checkboxolympics](https://github.com/skilleven/clickomat/tree/main/testcases/checkboxolympics)

On the Website https://checkboxolympics.com/ you can run the very simplyfied script of the testcase and get a score around 2.2 seconds...
