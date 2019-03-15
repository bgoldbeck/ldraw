# LScan

![LScan Logo](assets/images/lscan_256x256.bmp)


Travis CI [![Build Status](https://travis-ci.org/bgoldbeck/lscan.svg?branch=master)](https://travis-ci.org/bgoldbeck/lscan)


## What is this repository for? ##

* This repository contains the 2018-2019 capstone team project for computer science with professor Bart Massey.
* Find the documentation here: https://bgoldbeck.github.io/lscan/docs/index.html

## Dependencies ##
- [Python3](https://docs.python.org/3.6/)
- [PyOpenGL](http://pyopengl.sourceforge.net/)
- [WxPython](https://wxpython.org/)
- [Numpy](http://www.numpy.org/)
- [Numpy-STL](https://pypi.org/project/numpy-stl/)
- [Pyrr](https://pypi.org/project/pyrr/)
- [PyQuaternion](http://kieranwynn.github.io/pyquaternion/)
- [Pillow](https://pillow.readthedocs.io/en/stable/index.html)

## Setting up for Development ##

Before setting up this project, download latest version of Python3
- **Mac OS** 

    `$ brew install python3`
    
    (Note: If your Mac does not have `brew` visit https://brew.sh/ to install HomeBrew)
- **Windows OS**

    - Visit https://www.python.org/downloads/ to download latest version of Python3
    - Download latest Git Bash from https://git-scm.com/downloads


Follow the following steps to setup **LScan**


We recommend [PyCharm](https://www.jetbrains.com/pycharm/) for an IDE for this project. If you use pycharm you can skip step 2 and step 3. You can use PyCharm's settings to setup the environment.

## Setup Using PyCharm ##
1. Open PyCharm and load LScan project

2. Add Python interpreter.

    - Click `File` -> `Settings` -> `Project Interpreter`
    - Click :gear: and click `Add...`
    ![Add interpreter](assets/images/dev_setup/add_interpreter.png) 
    - Add base interpreter and click `OK`
    ![Base interpreter](assets/images/dev_setup/interpreter.PNG)
    
3. Follow these steps to install dependencies.
    - Open `requirements.txt`
    - Click `Install requirements` to top right corner.
    ![Install Dependencies](assets/images/dev_setup/install-packages.PNG)
    - A window with packages list appears. Select all and click `Install`
    ![Install](assets/images/dev_setup/install.PNG)

4. Right click `src/lscan.py` and click `Run` to test the environment setup.
   ![Run](assets/images/dev_setup/run_lscan.png)

5. Development environment is complete once LScan runs without any issues.
   ![LScan](assets/images/dev_setup/lscan.PNG)
   
### Mac OS ###
Open terminal and follow these steps.

1. From the terminal clone LScan repo

    `$ git clone https://github.com/bgoldbeck/lscan.git`

2. Change directory to **lscan**

    `$ cd lscan`

3. Install dependencies

    `$ pip install -r requirements.txt`
    

## Setup Without PyCharm ##  
Follow these steps if you are not using PyCharm.

### Windows OS ###

Open Git Bash and follow these steps.

1. Clone LScan repo

    `$ git clone https://github.com/bgoldbeck/lscan.git`

2. Change directory to **lscan**

    `$ cd lscan`

3. Install dependencies

    `$ pip install -r requirements.txt`
    

## How to Use LScan ###
![Using LScan](assets/images/using_lscan.gif)

## Bug Tracker ##
https://github.com/bgoldbeck/lscan/issues

# License

**LScan** is licensed under MIT License. Read [LICENSE](LICENSE) for license details. 

## Contact Us ##
Brandon Goldbeck: bpg@pdx.edu <br />
Anthony Namba: anamba@pdx.edu <br />
Brandon Le: lebran@pdx.edu <br />
Ann Peake: peakean@pdx.edu <br />
Sohan Tamang: sohan@pdx.edu <br />
Theron Anderson: atheron@pdx.edu <br />
An Huynh: anvanphuchuynh@gmail.com <br />

## Copyright ##
Copyright (C) 2018 
"Brandon Goldbeck", "Anthony Namba", "Brandon Le", "Ann Peake", "Sohan Tamang", "Theron Anderson", "An Huynh"
