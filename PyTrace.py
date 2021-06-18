import json
import multiprocessing
import sys
import random
import time
from multiprocessing import Pool


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from renderer import *
from scene import Scene
from sphere import Sphere


class PaintWidget(QWidget):
    def __init__(self, width, height, parent=None):
        super(PaintWidget, self).__init__(parent=parent)
        self.width = width
        self.height = height

        # setup an image buffer
        self.imgBuffer = QImage(self.width, self.height, QImage.Format_ARGB32_Premultiplied)
        self.imgBuffer.fill(QColor(0, 0, 0))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawImage(0, 0, self.imgBuffer)

    def sizeHint(self):
        return QSize(self.width, self.height)


class PyTraceMainWindow(QMainWindow):
    def __init__(self, qApp, width, height):
        super(PyTraceMainWindow, self).__init__()
        self.dock = QDockWidget("Dockable", self)
        self.two_done = False
        self.qApp = qApp
        self.width = width
        self.height = height
        self.gfxScene = QGraphicsScene()

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"PyTrace")
        self.resize(self.width + 130, self.height + 30)
        self.setWindowTitle("CENG488 PyTrace")
        self.setStyleSheet("background-color:black;")
        self.setAutoFillBackground(True)


        # set centralWidget
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName(u"CentralWidget")

        # create a layout to hold widgets
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # setup the gfxScene
        self.gfxScene.setItemIndexMethod(QGraphicsScene.NoIndex)

        # create a paint widget
        self.paintWidget = PaintWidget(self.width, self.height)
        self.paintWidget.setGeometry(QRect(0, 0, self.width, self.height))
        self.paintWidgetItem = self.gfxScene.addWidget(self.paintWidget)
        self.paintWidgetItem.setZValue(0)

        # create a QGraphicsView as the main widget
        self.gfxView = QGraphicsView(self.centralWidget)
        self.gfxView.setObjectName(u"GraphicsView")

        # assign our scene to view
        self.gfxView.setScene(self.gfxScene)
        self.gfxView.setGeometry(QRect(0, 0, self.width, self.height))

        # add widget to layout
        self.horizontalLayout.addWidget(self.gfxView)

        # set central widget
        self.setCentralWidget(self.centralWidget)

        # setup a status bar
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName(u"StatusBar")
        self.statusBar.setStyleSheet("background-color:gray;")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready...")
        w = QWidget(self)
        l = QVBoxLayout(w)
        self.pushButton1 = QPushButton("Render!")
        self.pushButton1.setStyleSheet("background-color: white")
        # inputDialog = QWidget(self)
        # inputDialog.setStyleSheet("background-color: white")
        # self.pushButton2, b = QInputDialog.getText(inputDialog, "sample", "ana")
        # a, c = QInputDialog.getText(inputDialog, "sample", "baba")
        l.addWidget(self.pushButton1)
        # l.addWidget(inputDialog)


        self.dock.setWidget(w)

        # self.pushButton.clicked.disconnect(self.buttonClick())

        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.setLayout(self.horizontalLayout)

    @staticmethod
    def buttonClick():
        print("Button clicked, Hello!")

    @staticmethod
    def renderMultiprocess(hmin):
        return hmin

    def resetBuffer(self):
        mainWindow.pushButton1.clicked.disconnect(mainWindow.renderBuffer)
        self.paintWidget.imgBuffer.fill(QColor(0, 0, 0))

    def renderBuffer(self):
        print("Updating buffer...")
        # randHue = random.random()
        AA = False
        # go through pixels
        start = time.time()
        for y in range(0, height):
            self.statusBar.showMessage(
                "{:.1f}%                    cpu count is:{}".format(y / self.height * 100, multiprocessing.cpu_count()))
            for x in range(0, width):
                if AA:
                    sub_samples = [renderer.render(scene, x + 0.25, y + 0.25),
                                   renderer.render(scene, x + 0.75, y + 0.25),
                                   renderer.render(scene, x + 0.25, y + 0.75),
                                   renderer.render(scene, x + 0.75, y + 0.75)]

                else:
                    sub_samples = [renderer.render(scene, x + 0.33, y + 0.33)]
                color = ColorRGBA(0, 0, 0, 1)
                for sample in sub_samples:
                    color += ColorRGBA(sample[0], sample[1], sample[2], 1)
                color = color/len(sub_samples)
                col = QColor.fromRgb(color.r, color.g, color.b)

                self.paintWidget.imgBuffer.setPixelColor(x, y, col)

            # update buffer
            # for z in range(0, 1000):
            # 	pass
            self.updateBuffer()
            # don't wait for the task to finish to update the view
            qApp.processEvents()
        end = time.time()
        print(end - start)

    def updateBuffer(self):
        self.paintWidget.update()


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @Slot()  # QtCore.Slot
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)


if __name__ == "__main__":
    # setup a QApplication
    qApp = QApplication(sys.argv)
    qApp.setOrganizationName("CENG488")
    qApp.setOrganizationDomain("cavevfx.com")
    qApp.setApplicationName("PyTrace")

    global scene
    scene = Scene()
    with open('render_settings.json', 'r') as file:
        render_settings = json.loads(file.read())

        RENDER_WIDTH = render_settings["renderSettings"]["xres"]
        RENDER_HEIGHT = render_settings["renderSettings"]["yres"]
        SAMPLES = render_settings["renderSettings"]["samples"]
        CAM_POS = render_settings["camera"]["position"]
        for sphereSettings in render_settings["spheres"]:
            sphere = Sphere.load(sphereSettings)
            scene.addNode(sphere)
        for lightSettings in render_settings["lights"]:
            light = Sphere.load(lightSettings, "light")
            scene.addLight(light)

    global renderer
    renderer = Renderer(
        width=RENDER_WIDTH,
        height=RENDER_HEIGHT,
        sample_count=SAMPLES,
        camera=Camera(Vector3f(
            CAM_POS[0],
            CAM_POS[1],
            CAM_POS[2]
        )
        )
    )

    # setup main ui
    width = 900
    height = 900
    mainWindow = PyTraceMainWindow(qApp, width, height)
    mainWindow.setupUi()

    mainWindow.show()
    mainWindow.pushButton1.clicked.connect(mainWindow.renderBuffer)

    # an example of writing to buffer

    # mainTimer = QTimer()
    # mainTimer.timeout.connect(mainWindow.timerBuffer)
    # mainTimer.start(1000)


    # enter event loop
    sys.exit(qApp.exec_())
