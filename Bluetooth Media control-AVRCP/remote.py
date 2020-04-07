'''
Copyright (C) <2020>  <Sai Prasanth.M>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import dbus
import dbus.service
import dbus.mainloop.glib
from bluetool import Bluetooth
from time import sleep

SERVICE_NAME = "org.bluez"
AGENT_IFACE = SERVICE_NAME + '.Agent1'
ADAPTER_IFACE = SERVICE_NAME + ".Adapter1"
DEVICE_IFACE = SERVICE_NAME + ".Device1"
PLAYER_IFACE = SERVICE_NAME + '.MediaPlayer1'
CONTROL_IFACE = SERVICE_NAME + '.MediaControl1'
TRANSPORT_IFACE = SERVICE_NAME + '.MediaTransport1'

class blue():
    def __init__(self):
        self.blue_t = Bluetooth()
        self.device = None
        self.address = None
        self.paired = False
        self.connected = False
    def get_paired(self):
        return self.blue_t.get_paired_devices()
    def get_connected(self):
        return self.blue_t.get_connected_devices()


class Remote():
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.paths = []
        self.iface = []
        self.play_path = None
        self.trans_path = None
        self.status = None
        self.track = None
        self.artist = None
        self.title = None
        self.album = None
        self.number = None
        self.total = None
        self.props_t = None
        self.path_t = None
        self.play_props = None
        self.trans_props = None
        self.dev_props = None

    def get_objects(self):
        self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")
        self.objects = self.manager.GetManagedObjects()    
        return self.objects    

    def find_adapter(self,objects):
        for path, ifaces in objects.items():
            adap = ifaces.get(ADAPTER_IFACE)
            if adap is None:
                continue
            self.obj = self.bus.get_object(SERVICE_NAME, path)
            self.adapter = dbus.Interface(self.obj, ADAPTER_IFACE)
            
        return self.adapter
        raise Exception("Bluetooth adapter not found")

    def get_player_path(self,objects):
        for path, interfaces in objects.items():
            self.paths.append(path)
            self.iface.append(interfaces)
            if PLAYER_IFACE in interfaces:
                self.play_path = path
        
        return self.play_path
        raise Exception("No media player has found")

    def get_transport_path(self,objects):
        for path, interfaces in objects.items():
            self.paths.append(path)
            self.iface.append(interfaces)
            if TRANSPORT_IFACE in interfaces:
                self.trans_path = path
        
        return self.trans_path
        raise Exception("No media transport has found")
    
    def get_control_path(self,objects):
        for path, interfaces in objects.items():
            self.paths.append(path)
            self.iface.append(interfaces)
            if CONTROL_IFACE in interfaces:
                self.control_path = path
        
        return self.control_path
        raise Exception("No media control has found")

    def next(self):
        self.player.Next(dbus_interface=PLAYER_IFACE)

    def fastforward(self):
        self.player.FastForward(dbus_interface=PLAYER_IFACE)

    def previous(self):
        self.player.Previous(dbus_interface=PLAYER_IFACE)

    def play(self):
        self.player.Play(dbus_interface=PLAYER_IFACE)

    def pause(self):
        self.player.Pause(dbus_interface=PLAYER_IFACE)

    def play_pause(self,state):
        if state == "playing":
            self.pause()
        if state == "paused":
            self.play()

    def rewind(self):
        self.player.Rewind(dbus_interface=PLAYER_IFACE)

    def shuffle(self,path,state):
        self.proxy = self.bus.get_object("org.bluez",path)
        self.shuf = dbus.Interface(self.proxy,"org.freedesktop.DBus.Properties")
        if state == 'off':
            self.shuf.Set(PLAYER_IFACE, "Shuffle", dbus.String('alltracks'))
        if state == 'alltracks':
            self.shuf.Set(PLAYER_IFACE, "Shuffle", dbus.String('off'))

    def repeat(self,path,state):
        self.proxy = self.bus.get_object("org.bluez",path)
        self.rep = dbus.Interface(self.proxy,"org.freedesktop.DBus.Properties")
        if state == 'off':
            self.rep.Set(PLAYER_IFACE, "Repeat", dbus.String('singletrack'))
        if state == 'singletrack':
            self.rep.Set(PLAYER_IFACE, "Repeat", dbus.String('off'))
            
    def volumeUp(self,path,volume):
        self.proxy = self.bus.get_object("org.bluez",path)
        self.volume = dbus.Interface(self.proxy,"org.freedesktop.DBus.Properties")
        self.inr = volume+10
        if self.inr < 127:
            self.volume.Set(TRANSPORT_IFACE, "Volume", dbus.UInt16(self.inr))
        else:
            self.volume.Set(TRANSPORT_IFACE, "Volume", dbus.UInt16(127))

    def set(self,path,interface,variant,state):
        self.proxy = self.bus.get_object("org.bluez",path)
        self.change = dbus.Interface(self.proxy,"org.freedesktop.DBus.Properties")
        self.change.Set(interface, variant, dbus.String(state))
    
    def volumeDown(self,path,volume):
        self.proxy = self.bus.get_object("org.bluez",path)
        self.volume = dbus.Interface(self.proxy,"org.freedesktop.DBus.Properties")
        self.dcr = volume-10
        if self.dcr > 10:
            self.volume.Set(TRANSPORT_IFACE, "Volume", dbus.UInt16(self.dcr))
        else:
            self.volume.Set(TRANSPORT_IFACE, "Volume", dbus.UInt16(0))

    def player(self,play_path):
        if play_path:
            self.connected = True
            self.player = self.bus.get_object("org.bluez", self.play_path)
            self.play_props = self.player.GetAll(PLAYER_IFACE, dbus_interface="org.freedesktop.DBus.Properties")

        return self.player,self.play_props

    def transport(self,trans_path):
        if trans_path:
            self.trans = self.bus.get_object("org.bluez", self.trans_path)
            self.trans_props = self.trans.GetAll(TRANSPORT_IFACE, dbus_interface="org.freedesktop.DBus.Properties")

        return self.trans, self.trans_props

    def device(self,play_path):
        self.player = self.bus.get_object("org.bluez", self.play_path)
        self.dev_path = self.player.Get(PLAYER_IFACE, "Device", dbus_interface="org.freedesktop.DBus.Properties")

        if self.dev_path:
            self.device = self.bus.get_object("org.bluez", self.dev_path)
            self.dev_props = self.device.GetAll(DEVICE_IFACE, dbus_interface="org.freedesktop.DBus.Properties")
            self.devAlias = self.device.Get(DEVICE_IFACE, "Alias", dbus_interface="org.freedesktop.DBus.Properties")

        return self.devAlias, self.dev_props, self.dev_path    

    def control(self,control_path):
        if control_path:
            self.control = self.bus.get_object("org.bluez", self.control_path)
            self.control_props = self.control.GetAll(CONTROL_IFACE, dbus_interface="org.freedesktop.DBus.Properties")

        return self.control, self.control_props
    

    def media_details(self,play_props):
        if "Status" in play_props:
            self.status = play_props["Status"]
        if "Track" in play_props:
            self.track = play_props["Track"]
        if "Artist" in self.track:
            self.artist = self.track["Artist"]
        if "Title" in self.track:
            self.title = self.track["Title"]
        if "Album" in self.track:
            self.album = self.track["Album"]
        if "TrackNumber" in self.track:
            self.number = self.track["TrackNumber"]
        if "NumberOfTracks" in self.track:
            self.total = self.track["NumberOfTracks"]
        
        return self.status,self.track,self.album,self.artist,self.title,self.number,self.total


    def options(self,play_props):
        if "Track" in play_props:
            self.track = play_props["Track"]
        if "Shuffle" in self.track:
            self.shuttle = self.track["Shuffle"]
        if "Repeat" in self.track:
            self.repeat = self.track["Repeat"]
            
        return self.shuttle,self.repeat

if __name__ == "__main__":
    blue = blue()
    paired = blue.get_paired()
    connected = blue.get_connected()
    print(paired)
    print("\n",connected)
    address = connected[0]
    address = address['mac_address'].decode('UTF-8')
    print(address)
