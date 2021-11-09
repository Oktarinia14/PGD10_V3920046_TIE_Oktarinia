from math import pi, sin, cos #untuk pergerakan kamera
from direct.showbase.ShowBase import ShowBase #mengambil dan menampilkan image dari framework ShowBase
from direct.task import Task #fungsi python (event handling)
from direct.actor.Actor import Actor #meload kelas aktor 
from direct.interval.IntervalGlobal import Sequence #memanipulasi waktu perpindahan/movement
from panda3d.core import Point3 #mengatur titik koordinat aktor
 
class MyApp(ShowBase):
    def __init__(self): 
        ShowBase.__init__(self) # menginisialisasi modul ShowBase

        # Nonaktifkan kontrol trackball kamera
        self.disableMouse()

        # load model lingkungan.
        self.scene = self.loader.loadModel("models/environment")
        # mengatur ulang model yang akan dirender
        self.scene.reparentTo(self.render) 
        # untuk mengatur skala dan posisi pada model
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # prosedur spinCameraTask pada task
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # meload dan mengubah aktor panda
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Looping pada actor panda yang diikuti dengan code "walk" sehingga panda dapat berjalan
        self.pandaActor.loop("walk")

        # Membuat empat posisi untuk panda berjalan 
        # berjalan maju mundur.
        posInterval1 = self.pandaActor.posInterval(13,
                                                   Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0))
        posInterval2 = self.pandaActor.posInterval(13,
                                                   Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0))
        hprInterval1 = self.pandaActor.hprInterval(3,
                                                   Point3(180, 0, 0),
                                                   startHpr=Point3(0, 0, 0))
        hprInterval2 = self.pandaActor.hprInterval(3,
                                                   Point3(0, 0, 0),
                                                   startHpr=Point3(180, 0, 0))

        # Memanggil posisi interval yang sudah dibuat tadi
        self.pandaPace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

    # Menentukan prosedur untuk memindahkan kamera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0 #angle degress untuk mencari sudut kamera 
        angleRadians = angleDegrees * (pi / 180.0) #angleRadians digunakan untuk mendapatkan nilai radian dari sudut kamera tersebut
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3) 
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

#inisialisasi Function MyApp() ke variabel app
app = MyApp()
#load Musik dengan memanggil musik sesuai dengan folder penyimpanan musik
mySound = app.loader.loadSfx("music\musik-bg.ogg")
#mutar Musik
mySound.play()
#Looping musik sehingga terus berulang
mySound.setLoop(True)
#Volume pada musik
mySound.setVolume(13)
#menjalankan aplikasi
app.run()