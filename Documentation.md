# Introduction #

Because PyNXC is a thin wrapper around the the NXC library, documentation for those projects will be very useful.  Of particular interest are
  1. The NXC Guide: http://bricxcc.sourceforge.net/nbc/nxcdoc/NXC_Guide.pdf
  1. The NXC Tutorial: http://bricxcc.sourceforge.net/nbc/nxcdoc/NXC_tutorial.pdf

All of the tutorial samples from the NXC tutorial are translated into PyNXC and can be found in the `tutorial_samples` folder.

# Simple program #
A simple program, out of the NXC Tutorial (Benedettelli, 2007) is the following program which moves forward until the touch-sensor (on NXT port 1) is pressed:

```
#include "NXCDefs.h" 
task main() 
{ 
  SetSensor(IN_1,SENSOR_TOUCH); 
  OnFwd(OUT_AC, 75); 
  until (SENSOR_1 == 1); 
  Off(OUT_AC); 
} 
```

The same code in PyNXC is:

```
def main():
    DefineSensors(TOUCH,None,None,None)
    OnFwd(OUT_AC, 75)
    while  SensorVal(1) != 1:
        pass
    Off(OUT_AC)
```

The structure of the program is a the same, but there are no `#include` directives, or semicolons.


# PyNXC Particulars #

## DefineSensors ##

The function `DefineSensors` is defined to easily set the various sensor values in an easy way.  The syntax for this function is

```
DefineSensors(PORT1,PORT2,PORT3,PORT4)
```
where the accepted values for the sensors in each port are `TOUCH`, `EYES`, `LIGHT`, `SOUND`, and `None`.


## Tasks, Inline, Subroutines ##

In every program there is a  function called `main` which gets called when the robot is told to run the program..  The NXT is a multitasking platform, where all of the initial tasks are started in the main program and are run concurrently.  In  NXC, tasks are denoted with a `task` keyword.  In PyNXC,

```
def task_foo():
    pass
```

is translated to NXC code:

```
task task_foo(){
}
```

In this way, the name of a function can determine what kind of NXC function is involved.  This convention works for functions declared as inline (e.g named `inline_foo`) and subroutines (e.g. named `sub_foo`).


## DEFINE ##

In NXC there is a pre-processor directive, `#DEFINE` which does a search-replace in the file before compilation.  Python doesn't have this, so I've added a keyword `DEFINE` which can be used like
```
DEFINE TURN_SPEED = 50
```

I think I want to change this in the future to be
```
DEFINE('TURN_SPEED','50')
```
to make it more clear that it is doing a string association.  A common mistake right now is:

```
DEFINE BAD = 10  # this comment gets inserted into code downstream
```

## Structs and Typedefs ##

NXC structs are implemented as Python classes, subclassing `Struct`.
```
class MyStruct(Struct):
    x=Byte(5)
    y=Word(6)
    s=String('hello')

m=MyStruct()

m2=MyStruct(x=6,y=7,s='this')
```

> Typedefs are implemented just like struct, by the Python subclassing syntax.
```
class MyByte(Byte):
    pass
```

## For-loops ##

For-loops work with limited forms range, not on lists (which don’t exist in NXC) or arrays (yet).

```
i=Byte()
s=String()

for i in range(256):
    s=NumToStr(i)

for i in range(1,12):
    s=NumToStr(i)

for i in range(1,12,3):
    s=NumToStr(i)
```


## Multiple Task example ##

This program is a more complex example of a robot which has to wander around looking for bins to through a ping-pong into. It uses a [behavioral program paradigm](http://en.wikipedia.org/wiki/Behavior_based_AI), and highlights many of the features of PyNXC:

```
DEFINE CRUISE_SPEED = 75
DEFINE TURN_SPEED = 50
DEFINE LIGHT_THRESHOLD = 33
DEFINE SHOOT_DISTANCE = 55
DEFINE MAX_DIST = 150
DEFINE QUARTER_TURN_TIME = 740
DEFINE DELAY_BEFORE_TURN = 950
DEFINE GOAROUND_DELAY_TIME = 800

do_shoot = 0
do_sweep_search = 0
do_stay_in_arena = 0
do_return = 0
do_go_around = 0
target_forward = 0
shot_ball = 0
done = 0
net_turn = 2
boxes_found = 0
boxes_passed = 0
    
def task_arbiter():
    
    while True:
        if do_go_around and do_return:
            OnFwd(OUT_C, TURN_SPEED)
            OnRev(OUT_B, TURN_SPEED)
            Wait(QUARTER_TURN_TIME)
            OnFwdReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
            while SensorVal(1) < 20:
                pass
            Wait(GOAROUND_DELAY_TIME)
            OnFwd(OUT_B, TURN_SPEED)
            OnRev(OUT_C, TURN_SPEED)
            Wait(QUARTER_TURN_TIME)
            OnFwdReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
            Wait(GOAROUND_DELAY_TIME)
            while SensorVal(1) < 20:
                pass
        elif do_return:
            # return to base
            OnFwdReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
            if SensorVal(4) == 1:
                Off(OUT_BC)
                Float(OUT_A)
                Wait(500)
                while SensorVal(4) == 0:
                    pass
                Wait(500)
                # big reset button
                do_shoot = 0
                do_sweep_search = 0
                do_stay_in_arena = 0
                do_return = 0
                do_go_around = 0
                target_forward = 0
                shot_ball = 0
                done = 0
                net_turn = 2
                boxes_passed = 0
                Off(OUT_A)
        elif do_stay_in_arena:
            OnFwdReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
            Wait(500)
            OnFwd(OUT_C, TURN_SPEED)
            OnRev(OUT_B, TURN_SPEED)
            Wait(QUARTER_TURN_TIME * 2)
            OnFwdReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
            Wait(750)
            do_stay_in_arena = False
            net_turn += 2
        elif do_go_around and boxes_passed < boxes_found:
            OnFwd(OUT_C, TURN_SPEED)
            OnRev(OUT_B, TURN_SPEED)
            Wait(QUARTER_TURN_TIME)
            OnFwdReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
            while SensorVal(1) < 20:
                pass
            Wait(GOAROUND_DELAY_TIME)
            OnFwd(OUT_B, TURN_SPEED)
            OnRev(OUT_C, TURN_SPEED)
            Wait(QUARTER_TURN_TIME - 50)
            OnFwdReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
            Wait(GOAROUND_DELAY_TIME)
            while SensorVal(1) < 20:
                pass
            Wait(500)
            boxes_passed += 1
            target_forward = False
        elif do_shoot:
            # shoot ball
            OnRevReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
            Wait(950)
            Off(OUT_BC)
            Wait(500)
            RotateMotor(OUT_A, 100, -25)
            Off(OUT_A)
            shot_ball = True
            boxes_found += 1
            OnFwd(OUT_B, TURN_SPEED)
            OnRev(OUT_C, TURN_SPEED)
            for i in range(net_turn):
                Wait(QUARTER_TURN_TIME)
        elif do_sweep_search:
            #scan for boxes
            OnFwdReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
            if SensorVal(1) < MAX_DIST and not target_forward:
                if boxes_passed < boxes_found:
                    boxes_passed += 1
                    while SensorVal(1) < MAX_DIST and SensorVal(2) == 0:
                        pass
                else:
                    # turn towards box and continue
                    Wait(DELAY_BEFORE_TURN)
                    PlayToneEx(262,400,7,False);  Wait(100)
                    OnFwd(OUT_B, TURN_SPEED)
                    OnRev(OUT_C, TURN_SPEED)
                    Wait(QUARTER_TURN_TIME)
                    net_turn -= 1
                    OnFwdReg(OUT_BC, CRUISE_SPEED, OUT_REGMODE_SYNC)
                    target_forward = True
            if SensorVal(2) == 1:
                PlayToneEx(330,400,7,False);  Wait(100)
    
    Off(OUT_BC)
                    
def task_sweep_search():

    while True:
        do_sweep_search = True
        
def task_stay_in_arena():

    while True:
        if SensorVal(3) < LIGHT_THRESHOLD:
            do_stay_in_arena = True
            PlayToneEx(200,400,7,False);  Wait(100)
            Wait(500)
        else:
            do_stay_in_arena = False
    
def task_shoot():

    while True:
        if SensorVal(2) == 1:
            do_shoot = True
            done_shooting = True
        else:
            do_shoot = False
            
def task_return():

    while True:
        do_return = shot_ball
        
def task_go_around():
    
    while True:
        if SensorVal(2) == 1:
            do_go_around = True
            Wait(250)
        else:
            do_go_around = False
            
def main():

    DefineSensors(EYES, TOUCH, LIGHT, TOUCH)
    Off(OUT_BC)
    Precedes(task_arbiter, task_sweep_search, 
             task_stay_in_arena, task_go_around, 
             task_shoot, task_return)
             
```