import argparse
import pulsectl
import dbus

icons     = ['volume_mute', 'volume_down', 'volume_up', 'volume_off'] # Last icon is used for mute icon
width     = 20 
charEmpty = '_' 
charFull  = '█'
charMute  = '░'
step      = 0.05

notifyTimeout = 3000
notifyID      = 2593

parser = argparse.ArgumentParser(description='pyvolctrl')
parser.add_argument('action',    choices=['inc', 'dec', 'togglemute'])
parser.add_argument('--step',    type=int, help='How many percent volume is to be changed (default: 5)')
parser.add_argument('--width',   type=int, help='Full width of the bar (default: 20)')
parser.add_argument('--timeout', type=int, help='Notification timeout in milliseconds (default: 3000)')
args = parser.parse_args()

if args.step: step = abs(args.step) / 100
if args.width: width = abs(args.width)
if args.timeout: notifyTimeout = abs(args.timeout)

with pulsectl.Pulse('') as pulse:
    sink = 0
    
    for i in pulse.sink_list():
        if i.name == pulse.server_info().default_sink_name:
            sink = i
    
    muted = int(sink.mute)
    percentage = round(sink.volume.value_flat * 100)

    if args.action == 'inc':
        dif = (100 - percentage) / 100
        step = min(dif, step)
        pulse.volume_change_all_chans(sink, +step)

    if args.action == 'dec':
        pulse.volume_change_all_chans(sink, -step)


    percentage = round(sink.volume.value_flat * 100) # Update

    if args.action == 'togglemute': 
        if muted == 0:
            pulse.mute(sink, mute=True)
        else:
            pulse.mute(sink, mute=False)

        muted = 1 - muted # Mute state was changes, so invert

def icon():
    arrlen = len(icons) - 1 # -1 because last icon is used for mute
    clamped = int(round(percentage - 1) / (100 / arrlen))

    if muted: return icons[len(icons) - 1]
    else:     return icons[clamped]

def bar():
    retStr = str(percentage) + "%   "

    for i in range(0, width):
        if i < int(percentage * width / 100):
            if muted: retStr += charMute
            else:     retStr += charFull
        else:
            retStr += charEmpty

    return retStr


# Notification
item = "org.freedesktop.Notifications"

notifyInterface = dbus.Interface(dbus.SessionBus().get_object(item, "/"+item.replace(".", "/")), item)

#                      app name,    id,       icon,   title,  body,  actions,  hints,          timeout
notifyInterface.Notify("pyvolctrl", notifyID, icon(), bar(),  "",    [],       {"urgency": 1}, notifyTimeout)
