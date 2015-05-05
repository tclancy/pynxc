# Requirements #

PyNXC has been tested with the following versions, although other versions may work as well.

  * Python 2.5 or 2.6: http://www.python.org
  * wxPython 2.8.7.1:  http://www.wxpython.org/


I usually just install the [Enthought Edition of Python](http://www.enthought.com/products/epd.php), for all of my projects, which is a 1-click install of all of the libraries you will ever need.  :-)

If you want the latest NXC, then you'll need:
  * Not Exactly C (NBC/NXC 1.2.1):  http://bricxcc.sourceforge.net/nbc/
PyNXC comes with a version of NXC included for Windows, OS X, and Linux.


# Installation #

PyNXC comes with a binary for NXC version 1.0.1 b36 for Windows, OS X and Linux.  If you want to upgrade to the latest binaries, see below at [GettingStarted#Upgrading\_the\_NXC\_binary](GettingStarted#Upgrading_the_NXC_binary.md)



# Running PyNXC #

## GUI ##

Double-click on the pynxc.pyw file to run the GUI interface.  It should open a window with the current NXC information on it, something like:
```
PyNXC Version (0,1,6)
Firmware Version 105
Next Byte Codes Compiler version 1.2 (1.2.1.r1, built Wed Apr 14 05:13:37 CDT 2010)
     Copyright (c) 2006-2010, John Hansen
Use "nbc -help" for more information.
```

You can open a file with the File/Open menu, and then Compile and Download with the Program/Compile and Download menu.  Any errors will display in the window.

## Command line ##

Compiling and download can be done with a single line

```
$ ./pynxc.pyx --download program_name.py
```

A full list of commandline options is given by

```
$ ./pynxc -h
Usage: pynxc.pyw [options] [filename]

Options:
  -h, --help           show this help message and exit
  -c, --compile        compile to nxc code only
  --debug              show debug messages
  --show_nxc           show the nxc code
  -d, --download       download program
  -B, --bluetooth      enable bluetooth
  --firmware=FIRMWARE  firmware version (105, 107, or 128)
  --command=<command>  what is the nxc/nqc command
```



# Upgrading the NXC binary #

The only step to upgrading NXC is to get the binary for NXC in the correct folder.

## Windows ##

  1. Download NXC at http://bricxcc.sourceforge.net/nbc/release/nbc-1.2.1.r1.zip and extract it.  (If the link doesn't work, you can get the previous test release at http://bricxcc.sourceforge.net/test_release.zip)
  1. Copy the `nbc.exe` file to the `pynxc/nxc/win32` folder

## Mac OS X ##


  1. Download the Universal Binary at http://bricxcc.sourceforge.net/nbc/release/nbc-1.2.1.r1.osx.tgz
  1. Double-click on the file to extract the files, and open the resulting `nbc-1.2.1.r1.osx` folder
  1. In the `NXT` folder double-click on the file `nxtcom_scripts.zip` to unzip it.
  1. There are two files that you need to copy into the `pynxc/nbc/darwin` folder:
    1. `nbc` - which you can find in the `NXT` folder
    1. `nxtcom` - which you can find in the `nxtcom-scripts` folder

## Linux ##

  1. Download NXC at http://bricxcc.sourceforge.net/nbc/release/nbc-1.2.1.r1.tgz and extract it
  1. Copy the file `nxc` from the `NXT` folder into anywhere in your path, or in the `pynxc/nxc/linux2` folder