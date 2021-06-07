# CENG 488 Assignment2 by
# Onur Ozcan
# StudentId:240201032
# 5 2021

class Scene:
    def __init__(self):
        self.objects = []
        self.lights = []

    def addNode(self, node):
        self.objects.append(node)

    def addLight(self, light):
        self.lights.append(light)
