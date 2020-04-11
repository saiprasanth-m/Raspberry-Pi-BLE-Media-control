from PyQt4 import QtGui
import sys
import remote
from time import sleep

class App(QtGui.QMainWindow):
    def __init__(self):
        super(App,self).__init__()
        self.display()   

    def display(self):
        self.w = QtGui.QWidget()
        self.w.resize(1000,300)
        self.w.setWindowTitle("Remote_GUI")
        
        self.l1 = QtGui.QLabel(self.w)
        self.l1.setText("Remote control")
        self.l1.move(110+40,15)

        self.l2 = QtGui.QLabel(self.w)
        self.l2.move(400,15)
        
        self.l4 = QtGui.QLabel(self.w)
        self.l4.move(400,80)

        self.l3 = QtGui.QLabel(self.w)
        self.l3.move(400,45)
        
        self.b1 = QtGui.QPushButton("",self.w)
        self.b1.move(120+40,45)
        self.b1.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/volume-plus-256.png")))
        self.b1.resize(80,30)
        
        self.b2 = QtGui.QPushButton("",self.w)
        self.b2.move(120+40,135)
        self.b2.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/volume-minus-512.png")))
        self.b2.resize(80,30)
        
        self.b3 = QtGui.QPushButton("",self.w)
        self.b3.move(50+40,90)
        self.b3.resize(40,30)
        self.b3.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/previous.png")))
        
        self.b4 = QtGui.QPushButton("",self.w)
        self.b4.move(240+40,90)
        self.b4.resize(40,30)
        self.b4.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/next.png")))

        self.b5 = QtGui.QPushButton("",self.w)
        self.b5.move(100+40,90)
        self.b5.resize(130,35)
        self.b5.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/pause.png")))

        self.b7 = QtGui.QPushButton("",self.w)
        self.b7.move(70+40,200)
        self.b7.resize(80,30)
        self.b7.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/shuffle.png")))
        
        self.b8 = QtGui.QPushButton("",self.w)
        self.b8.move(183+40,200)
        self.b8.resize(80,30)
        self.b8.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/repeat.png")))

        self.b9 = QtGui.QPushButton("",self.w)
        self.b9.move(0+40,90)
        self.b9.resize(40,30)
        self.b9.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/rewind.png")))

        self.b10 = QtGui.QPushButton("",self.w)
        self.b10.move(290+40,90)
        self.b10.resize(40,30)
        self.b10.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/fast-forward.png")))


 
        self.b1.clicked.connect(self.VolumeUp)
        self.b2.clicked.connect(self.VolumeDown)
        self.b3.clicked.connect(self.Previous)
        self.b4.clicked.connect(self.Next)
        self.b5.clicked.connect(self.Play_Pause)
        self.b7.clicked.connect(self.Shuffle)
        self.b8.clicked.connect(self.Repeat)
        self.b9.clicked.connect(self.Rewind)
        self.b10.clicked.connect(self.FastForward)

        self.w.show()
        
    def details(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        adapter = media.find_adapter(objects)
        path = media.get_player_path(objects)
        path_T = media.get_transport_path(objects)

        player, props_P = media.player(path)
        device, props_D, path_D = media.device(path)
        transport, props_T = media.transport(path_T)
        status,track,album,artist,title,number,total_tracks = media.media_details(props_P)
        return status,track,album,artist,title,number,total_tracks

    def disp_status(self):
        status,track,album,artist,title,number,total_tracks = self.details()
        
        self.l2.setText(str(title))
        self.l3.setText(str(artist))
        self.l4.setText(str(album))
 
    def FastForward(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        adapter = media.find_adapter(objects)
        path = media.get_player_path(objects)
        path_T = media.get_transport_path(objects)

        player, props_P = media.player(path)
        media.fastforward()
        
    def Rewind(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        adapter = media.find_adapter(objects)
        path = media.get_player_path(objects)
        path_T = media.get_transport_path(objects)

        player, props_P = media.player(path)
        media.rewind()    

    def Next(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        adapter = media.find_adapter(objects)
        path = media.get_player_path(objects)
        path_T = media.get_transport_path(objects)

        player, props_P = media.player(path)
        media.next()
        sleep(0.5)
        self.disp_status()

    def Previous(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        adapter = media.find_adapter(objects)
        path = media.get_player_path(objects)
        path_T = media.get_transport_path(objects)

        player, props_P = media.player(path)
        media.previous()
        sleep(0.5)
        self.disp_status()
        
    def Shuffle(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        adapter = media.find_adapter(objects)
        path = media.get_player_path(objects)
        path_T = media.get_transport_path(objects)

        player, props_P = media.player(path)
        state = props_P["Shuffle"]
        print(state)
        if state == 'alltracks':
            self.b7.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/shuffle.png")))
            sleep(0.5)
        
        if state == 'off':
            self.b7.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/shuffle-red.png")))
            sleep(0.5)
            set_state = 'alltracks'
            media.shuffle(path,set_state)
            sleep(0.5)

        state = set_state    
        media.shuffle(path,state)    
        
    def Repeat(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        adapter = media.find_adapter(objects)
        path = media.get_player_path(objects)
        path_T = media.get_transport_path(objects)

        player, props_P = media.player(path)
        state = props_P["Repeat"]
        print(state)
        if state == 'singletrack':
            self.b8.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/repeat.png")))
        sleep(0.5)
        if state == 'off':
            self.b8.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/repeat-red.png")))
        
        media.repeat(path,state)
        
    def Play_Pause(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        adapter = media.find_adapter(objects)
        path = media.get_player_path(objects)
        path_T = media.get_transport_path(objects)

        player, props_P = media.player(path)
        state = props_P["Status"]
        if state == "playing":
            self.b5.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/Play.png")))
        if state == "paused":
            self.b5.setIcon(QtGui.QIcon(QtGui.QPixmap("Icons/pause.png")))
        media.play_pause(state)
        
    
    def VolumeUp(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        path_T = media.get_transport_path(objects)
        transport, props_T = media.transport(path_T)
        volume = int(props_T["Volume"])

        media.volumeUp(path_T,volume)

    def VolumeDown(self):
        media = remote.Remote()
        objects = media.get_objects()
        
        path_T = media.get_transport_path(objects)
        transport, props_T = media.transport(path_T)
        volume = int(props_T["Volume"])
        
        media.volumeDown(path_T,volume)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

