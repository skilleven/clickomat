from setuptools import setup
setup(
    name="clickomat",
    version='0.3.2',
    entry_points={
        'console_scripts': [
            'clickomat=clickomat:run'
        ]
    },
    author="skilleven (Torsten Hoeltge)",
    author_email="<hello@skilleven.com>",
    url="https://github.com/skilleven/clickomat",
    description='Python-Script for automated click-sequences and text entry',
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    license="MIT",
    py_modules=['clickomat'],
    package_dir={'':'src'},
    install_requires=['pyautogui', 'keyboard', 'opencv-python', 'pillow', 'click'],
    keywords=['python', 'mouse-automation', 'gui-testing', 'automation'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License"
    ]
)
