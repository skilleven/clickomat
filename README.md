![Clickomat](https://repository-images.githubusercontent.com/538182878/80262157-c719-4543-b85c-c77e26655a5f)



# Clickomat 0.3.2

Python-Script for automated click-sequences and text entry.

Building on top of the brilliant lib "pyautogui" by [Al Sweigart](https://github.com/asweigart)
it offers the possibility to perform mouse clicks, text input and more with very simplified commands.

The purpose of Clickomat is to map the sometimes relatively long python commands from pyautogui with short,
single-line commands that are processed in a simple text list.

## Installation 
[![PyPI](https://img.shields.io/badge/PyPI%20package-0.3.2-brightgreen?style=for-the-badge&logo=Pypi&logoColor=white)](https://pypi.org/project/clickomat/)



```
$ pip install clickomat
```

### Run Testscript

Open https://checkboxolympics.com/ in Firefox (Chrome should work also). \
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

### Run Clickomat


#### From command-line as CLI
If run directly from command-line Clickomat takes arguments like this:

```
$ clickomat -d C:/path/to/case/dir -c clicklist.txt -i imagefolder
```
Defaults would simply be '.','t1.txt','images' if called w/o arguments.

If you only like to change the clicklist-file:

```
$ clickomat -c clicklist.txt
```

Options:
```
  -version, -v, --version                 show version number

  -path, -p, --path                       set path of case, default: `.`

  -clicklist, -c, --clicklist             set clicklist file of case, default:`t1.txt`

  -images, -i, --images                   set image directory of case, default: `images`

  -confidence, -co, --confidence          set the accuracy of target detection - 
                                          only values from 0.0 to 1.0 allowed, default: 0.95

  -autoswitch, -a, --autoswitch           if set Clickomat will switch back to terminal
                                          after execution, default: False

  -silent, -s, --silent                   if set Clickomat gives no terminal feedback,
                                          default: False

  -step, -st, --step                      set the pause length between each command, default: 0.06

  -noswitch, -n, --noswitch               if set Clickomat will not execute switch commands
                                          unless they are marked with `!`

  -help, -h, --help                       Show help
```

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



## Parameters

You can change some default parameters:


```
c.confidence           = 0.95
c.autoswitch           = False
c.autoswitch_pause     = 1
c.logging              = True
c.step_pause           = 0.06
c.switch_pause         = 0
c.switch               = True
```
* `confidence` - how accurate the target detector works
* `autoswitch` - if True a TAB-switch is performed after script execution
* `autoswitch_pause` - pause before autoswitch in seconds
* `logging` - if True a detailed log of the activities is printed while execution
* `step_pause` - minimum pause between every step in seconds 
* `switch_pause` - pause after a normal switch command in seconds
* `switch` - if False no switches are performed at all



---


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
| Command | Shorthand
|---|---
| **switch**                                |  >
| **click**                                 |  c
| **doubleclick**                           |  dc
| **shiftclick**                            |  sc
| **mdown**                                 |  md 
| **mup**                                   |  mu 
| **posX**                                  |  x
| **posY**                                  |  y
| **right**                                 |  r
| **left**                                  |  l
| **up**                                    |  u
| **down**                                  |  d
| **await**                                 |  a
| **write**                                 |  w
| **enter**                                 |  .
| **scroll**                                |  sl
| **del**                                   |  d
| **del dir**                               |  dd
| **lookup**                                |  lu


More commands coming...

# [Full Documentation](https://github.com/skilleven/clickomat/wiki)

---

## Dependencies:

```
* pyautogui
* keyboard
* opencv-python (on windows pyautogui works only with opencv)
* pillow (on windows pyautogui works only with pillow)
```

---

## Examples:
- [examplescript.txt](https://github.com/skilleven/clickomat/blob/main/examplescript.txt)
- Testcase: [checkboxolympics](https://github.com/skilleven/clickomat/tree/main/testcases/checkboxolympics)

On the Website https://checkboxolympics.com/ you can run the very simplyfied script of the testcase and get a score around 2.2 seconds...
