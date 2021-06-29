# pyvolctrl

Simple volume notifier written in python.





## Usage

```
usage: pyvolctrl.py [-h] [--step STEP] [--width WIDTH] [--timeout TIMEOUT] {inc,dec,togglemute}

pyvolctrl

positional arguments:
  {inc,dec,togglemute}

optional arguments:
  -h, --help            show this help message and exit
  --step STEP           How many percent volume is to be changed (default: 5)
  --width WIDTH         Full width of the bar (default: 20)
  --timeout TIMEOUT     Notification timeout in milliseconds (default: 3000)

```



Bind to keyboard volume buttons. In this example xbindkeys config file:

```
"python /path/to/pyvolctrl/pyvolctrl.py --step 10 inc"
   XF86AudioRaiseVolume

"python /path/to/pyvolctrl/pyvolctrl.py --step 10 dec"
   XF86AudioLowerVolume

"python /path/to/pyvolctrl/pyvolctrl.py togglemute"
   XF86AudioMute
```



## Dependencies

Pyvolctrl requires the following python packages:

- argparse
- subprocess
- pulsectl

