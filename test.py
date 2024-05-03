from monitorcontrol import get_monitors
from time import sleep

for monitor in get_monitors():
     with monitor:
         monitor.set_power_mode(4) # soft off
         sleep(3)
         monitor.set_power_mode(1) # on