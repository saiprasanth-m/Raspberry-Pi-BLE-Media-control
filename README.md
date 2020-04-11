# Bluetooth Media Control-AVRCP

Controlling any bluetooth media device that is connected to [*Raspberry Pi*](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) where Pi acts as a remote controller. Any media playing in the device connected to the raspberry pi via bluetooth can be controlled with the program written. The program contains two part where the linkage of d-bus and Pi's bluetooth found in [*remote.py*](https://github.com/saiprasanth-m/Raspberry-Pi/blob/master/Bluetooth%20Media%20control-AVRCP/remote.py) and a simple media player GUI can be found in [*GUI.py*](https://github.com/saiprasanth-m/Bluetooth-Media-control-AVRCP/blob/master/GUI.py)

# D-Bus

[*D-Bus*](https://en.wikipedia.org/wiki/D-Bus) is a software bus and an inter-process communication which allows communication between multiple processes running concurrently on the same machine. D-Bus was developed as part of the freedesktop.org project and further details can be found here (https://www.freedesktop.org/wiki/Software/dbus/). D-bus python API is used to connect with the bluez service on the pi and the official documentation of dbus-python is found here https://dbus.freedesktop.org/doc/dbus-python/tutorial.html


# Bluez

[*Bluez*](http://www.bluez.org/) is the Linux Bluetooth system and allows a Raspberry Pi to communicate with Bluetooth classic and Bluetooth low energy (LE) devices. Here, bluez tool is used to enable implementation of Bluetooth Low Energy (BLE) profiles such as AVRCP/A2DP where [*AVRCP*](https://www.bluetooth.com/) profile is used to control media(audio/video) communicated via bluetooth.


# Installation

1. To install bluez on raspberry pi, find here https://learn.adafruit.com/install-bluez-on-the-raspberry-pi/installation for step-by-step procedure of proper installation.
2. To install dbus-python, use "sudo apt-get install python-dbus" command
3. To install PyQt GUI toolkit, use "sudo apt-get install python-qt4" command

Dependencies:

1. bluez >= 5.0
2. dbus-python >= 1.2.8
3. PyQt >= 4
