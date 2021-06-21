import json
import multiprocessing
import sys
import random
import time
from multiprocessing import Pool, Process

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
        self.dock = QDockWidget("Settings", self)
        self.two_done = False
        self.qApp = qApp
        self.width = width
        self.height = height
        self.gfxScene = QGraphicsScene()

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"PyTrace")
        self.resize(self.width + 400, self.height + 50)
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

        # dock
        dockItems = QWidget(self)
        self.leftDock = QFormLayout(dockItems)
        dockItems.setStyleSheet("background-color: gray")

        # sub sample size selection box
        self.ssSize = QComboBox(self)
        self.ssSize.setStyleSheet("""
        background-color:white;
        font-family: Titillium;
        """)

        self.ssSize.addItems(["1", "2", "4"])
        self.leftDock.addRow("Subsample Size:", self.ssSize)


        self.ambientOn = QCheckBox("Ambient On")
        self.ambientOn.setChecked(True)
        self.leftDock.addRow(self.ambientOn)

        self.ambientStrength = QDoubleSpinBox()
        self.ambientStrength.setSingleStep(0.01)
        self.ambientStrength.setValue(0.15)
        self.ambientStrength.setMaximum(0.5)
        self.ambientStrength.setMinimum(0.0)
        self.leftDock.addRow(self.ambientStrength)

        # ambient sample size
        self.aoSize = QComboBox(self)
        self.aoSize.setStyleSheet("background-color:white;")
        self.aoSize.addItems(["2", "4", "8", "16", "32", "64"])
        self.leftDock.addRow("AO Sample Size:", self.aoSize)

        self.diffuseOn = QCheckBox("Diffuse On")
        self.diffuseOn.setChecked(True)
        self.leftDock.addRow(self.diffuseOn)

        self.diffuseStrength = QDoubleSpinBox()
        self.diffuseStrength.setSingleStep(0.05)
        self.diffuseStrength.setValue(0.6)
        self.diffuseStrength.setMaximum(2.0)
        self.diffuseStrength.setMinimum(0.0)
        self.leftDock.addRow(self.diffuseStrength)

        self.specularOn = QCheckBox("Specular On")
        self.specularOn.setChecked(True)
        self.leftDock.addRow(self.specularOn)
        # text

        self.sIntensity = QLabel("Specular Intensity")
        self.leftDock.addRow(self.sIntensity)

        self.specularStrength = QDoubleSpinBox()
        self.specularStrength.setValue(0.25)
        self.specularStrength.setSingleStep(0.05)
        self.specularStrength.setMaximum(2.0)
        self.specularStrength.setMinimum(0.0)
        self.leftDock.addRow(self.specularStrength)

        self.sRoughness = QLabel("Roughness")
        self.leftDock.addRow(self.sRoughness)

        self.specularRoughness = QSpinBox()
        self.specularRoughness.setValue(4)
        self.specularRoughness.setSingleStep(16)
        self.specularRoughness.setMaximum(256)
        self.specularRoughness.setMinimum(0)
        self.leftDock.addRow(self.specularRoughness)

        # render button
        self.renderButton = QPushButton("Render!")
        self.renderButton.setStyleSheet("background-color: white; ")

        self.leftDock.addRow(self.renderButton)

        self.text = QLabel("Three types of objects in this scene.\nMatte, Mirror, Glass, Light\n"
                           "Changing lighting values\nwill change it for\nall matte objects")
        self.leftDock.addRow(self.text)

        self.dock.setWidget(dockItems)

        # self.pushButton.clicked.disconnect(self.buttonClick())

        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.setLayout(self.horizontalLayout)

    def ambientValChanged(self):
        renderer.ambient_strength = self.ambientStrength.value()

    def diffValChanged(self):
        renderer.diffuse_strength = self.diffuseStrength.value()
        # print(self.diffuseStrength.value())

    def specValChanged(self):
        renderer.specular_strength = self.specularStrength.value()

    def ambientChanged(self):
        renderer.ambientOn = self.ambientOn.isChecked()
        if renderer.ambientOn:
            self.ambientStrength.show()
            self.aoSize.show()

        else:
            self.ambientStrength.hide()
            self.aoSize.hide()

    def roughnessChanged(self):
        renderer.specular_roughness = self.specularRoughness.value()

    def specularChanged(self):
        renderer.specularOn = self.specularOn.isChecked()
        if renderer.specularOn:
            self.specularStrength.show()
            self.specularRoughness.show()
        else:
            self.specularStrength.hide()
            self.specularRoughness.hide()

    def diffuseChanged(self):
        renderer.diffuseOn = self.diffuseOn.isChecked()
        if renderer.diffuseOn:
            self.diffuseStrength.show()
        else:
            self.diffuseStrength.hide()

    def selectionChange(self):
        for count in range(self.ssSize.count()):
            self.ssSize.itemText(count)

    def aoChange(self, i):
        for count in range(self.aoSize.count()):
            self.aoSize.itemText(count)
        renderer.SAMPLE_COUNT = int(self.aoSize.currentText())

    def resetBuffer(self):
        mainWindow.renderButton.clicked.disconnect(mainWindow.renderBuffer)
        self.paintWidget.imgBuffer.fill(QColor(0, 0, 0))

    def renderBuffer(self):
        print("Updating buffer...")
        # randHue = random.random()
        sub_sample = int(self.ssSize.currentText())
        # go through pixels
        start = time.time()

        for y in range(0, height):
            self.statusBar.showMessage(
                "{:.1f}% Done.".format(y / self.height * 100))
            for x in range(0, width):
                if sub_sample == 4:
                    sub_samples = [renderer.render(scene, x + 0.25, y + 0.25),
                                   renderer.render(scene, x + 0.75, y + 0.25),
                                   renderer.render(scene, x + 0.25, y + 0.75),
                                   renderer.render(scene, x + 0.75, y + 0.75)]
                elif sub_sample == 2:
                    sub_samples = [renderer.render(scene, x + 0.33, y + 0.33),
                                   renderer.render(scene, x + 0.66, y + 0.66)]

                else:
                    sub_samples = [renderer.render(scene, x + 0.5, y + 0.5)]
                color = ColorRGBA(0, 0, 0, 1)
                for sample in sub_samples:
                    color += ColorRGBA(sample[0], sample[1], sample[2], 1)
                color = color / len(sub_samples)
                col = QColor.fromRgb(color.r, color.g, color.b)

                self.paintWidget.imgBuffer.setPixelColor(x, y, col)

            # update buffer
            # for z in range(0, 1000):
            # 	pass
            self.updateBuffer()
            # don't wait for the task to finish to update the view
            qApp.processEvents()
        self.statusBar.showMessage("Rendering Done.")
        end = time.time()
        print(end - start)

    def updateBuffer(self):
        self.paintWidget.update()


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
    mainWindow.renderButton.clicked.connect(mainWindow.renderBuffer)
    mainWindow.ssSize.currentIndexChanged.connect(mainWindow.selectionChange)
    mainWindow.aoSize.currentIndexChanged.connect(mainWindow.aoChange)
    mainWindow.ambientOn.stateChanged.connect(mainWindow.ambientChanged)
    mainWindow.diffuseOn.stateChanged.connect(mainWindow.diffuseChanged)
    mainWindow.specularOn.stateChanged.connect(mainWindow.specularChanged)
    mainWindow.diffuseStrength.valueChanged.connect(mainWindow.diffValChanged)
    mainWindow.specularStrength.valueChanged.connect(mainWindow.specValChanged)
    mainWindow.ambientStrength.valueChanged.connect(mainWindow.ambientValChanged)
    mainWindow.specularRoughness.valueChanged.connect(mainWindow.roughnessChanged)
    # an example of writing to buffer

    # mainTimer = QTimer()
    # mainTimer.timeout.connect(mainWindow.timerBuffer)
    # mainTimer.start(1000)

    # enter event loop
    sys.exit(qApp.exec_())
