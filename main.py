# CENG 488 Assignment2 by
# Onur Ozcan
# StudentId:240201032
# 5 2021

import time
import json

from camera import Camera
from renderer import Renderer
from scene import Scene
from sphere import Sphere
from vector import *


def main():
    scene = Scene()
    with open('render_settings.json', 'r') as file:
        render_settings = json.loads(file.read())

        RENDER_WIDTH = render_settings["renderSettings"]["xres"]
        RENDER_HEIGHT = render_settings["renderSettings"]["yres"]
        SAMPLES = render_settings["renderSettings"]["samples"]
        CAM_POS = render_settings["camera"]["position"]

        sphere1 = Sphere.load(render_settings["sphere1"])

        sphere2 = Sphere.load(render_settings["sphere2"])
        sphere3 = Sphere.load(render_settings["sphere3"])
        sphere4 = Sphere.load(render_settings["sphere4"])
        light1 = Sphere.load(render_settings["light1"], "light")
        ground = Sphere.load(render_settings["ground"])
    # sphere1.color = ColorRGBA(1, 0, 0, 1)
    # sphere2.color = ColorRGBA(0, 1, 0, 0)
    # ground.color = ColorRGBA(0, 0, 1, 0)
    sphere1.material = 1
    sphere2.material = 100
    scene.addNode(sphere1)
    scene.addNode(sphere2)
    scene.addNode(sphere3)
    scene.addNode(sphere4)
    scene.addNode(light1)
    scene.addLight(light1)
    print(light1.type)
    print(sphere1.type)
    # scene.addNode(sphere3)
    scene.addNode(ground)

    start = time.time()

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
    name = 'output.png'
    renderer.render(scene)
    renderer.writeTo()
    # data = numpy.asarray(renderer.render_multiprocess(scene, 11))
    # data = data.reshape(1000, 1000, 3)
    # img = Image.fromarray(data, 'RGB')
    # img.save(name)
    # Image.open(name).show()

    print("Rendering Done!")
    t = time.time() - start
    print("Width:{}\nHeight:{}\n{} Samples\nRendered in:{:.0f} min {:.1f} sec".format(RENDER_WIDTH, RENDER_HEIGHT,
                                                                                      SAMPLES,
                                                                                      t // 60, t % 60))
    print("Saved output.png")


if __name__ == '__main__':
    main()
