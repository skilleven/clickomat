from setuptools import setup

VERSION = '0.1.2'
DESCRIPTION = 'Python-Script for automated click-sequences and text entry'
LONG_DESCRIPTION = 'The purpose of Clickomat is to map the sometimes relatively long python commands from pyautogui with short, single-line commands that are processed in a simple text list.'

# Setting up
setup(
    name="clickomat",
    version=VERSION,
    author="skilleven (Torsten Hoeltge)",
    author_email="<hello@skilleven.com>",
    url="https://github.com/skilleven/clickomat",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    py_modules=['clickomat'],
    package_dir={'':'src'},
    install_requires=['pyautogui', 'keyboard', 'easygui', 'opencv-python', 'pillow'],
    keywords=['python', 'mouse-automation', 'gui-testing', 'automation'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License"
    ]
)