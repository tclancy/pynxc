# Welcome to PyNXC! #

PyNXC is a  project which converts python code to "Not Exactly C" (NXC) (http://bricxcc.sourceforge.net/nbc/) code, to download to LEGO MINDSTORMS Robots.

## PyNXC at a Glance ##

The following program moves the robot forward until the touch sensor (bumper) on port 1 is pressed:
```
def main():
    DefineSensors(TOUCH,None,None,None)
    OnFwd(OUT_AC, 75)
    while  SensorVal(1) != 1:
        pass
    Off(OUT_AC)
```

Compiled and downloaded to the robot with:

```
$ ./pynxc --download program_name.py
```


## PyNXC GUI Interface ##

PyNXC also provides a simple GUI interface to load files, and download them to the robot.  Error messages are displayed in the window.

Run without any options


```
$ ./pynxc
```

or simply double-click on the PyNXC file.

## Getting Started ##

To start using PyNXC and see what you can do with it, go to the GettingStarted page, and the Documentation page.