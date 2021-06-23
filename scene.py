# CENG 488 Assignment 8 by
# Onur Ozcan
# StudentId:240201032
# 6 2021

class Scene:
    def __init__(self):
        self.objects = []
        self.lights = []

    def addNode(self, node):
        self.objects.append(node)

    def addLight(self, light):
        self.objects.append(light)
        self.lights.append(light)
