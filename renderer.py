# CENG 488 Assignment2 by
# Onur Ozcan
# StudentId:240201032
# 5 2021
"""
References:
    Finding the normal aligned hemisphere:
        https://www.scratchapixel.com/lessons/3d-basic-rendering/global-illumination-path-tracing/global-illumination-path-tracing-practical-implementation
    Ray Sphere Intersection:
        https://www.youtube.com/watch?v=KaCe63v4D_Q&ab_channel=ArunRavindranArunRocks
    Better Sampling:
        http://www.rorydriscoll.com/2009/01/07/better-sampling/

"""

import math
import random
from math import sin, cos

import numpy as np
from PIL import Image
from multiprocessing import Array
from camera import Camera
from ray import Ray
from vector import Point3f, ColorRGBA, Vector3f


class Renderer(object):
    def __init__(self, width, height, sample_count=20, camera=Camera()):
        self.width = width
        self.height = height
        # color of each pixel
        self.data = np.zeros((height, width, 3), dtype=np.uint8)
        self.SAMPLE_COUNT = sample_count
        self.samples = []
        self.camera = camera
        self.shared_data = Array("i", self.width * self.height * 3)
        self.uniforms = []
        # self.generateUniform()
        # self.createSamples()

    def render(self, scene, x, y):
        """
        This function will find the colors for each pixel on the rendered image in old school fashion.
        It spans the screen horizontally and vertically and finds color of the each pixel by shooting a ray.
        :param y:
        :param x:
        :param scene: takes a scene that keeps sphere
        :return:
        """

        def to_byte(c):
            """
            :param c: value [0, 1]
            :return: value [0, 255]
            """
            return round(max(min(c * 255, 255), 0))

        aspect_ratio = float(self.width) / self.height
        # near plane borders
        x0 = -1
        x1 = 1
        y0 = -1.0 / aspect_ratio
        y1 = +1.0 / aspect_ratio
        # step sizes
        x_pixel = (x1 - x0) / (self.width - 1)
        y_pixel = (y1 - y0) / (self.height - 1)

        image_y = y0 + y * y_pixel
        image_x = x0 + x * x_pixel

        ray = Ray(origin=self.camera.camPosition, direction=Point3f(image_x, image_y, 1) - self.camera.camPosition)
        clr = self.trace(ray, scene)
        return to_byte(clr.r), to_byte(clr.g), to_byte(clr.b)
        # for each column
        # for y in range(0, self.height):
        #     print("{:.1f}%".format(y / self.height * 100))
        #     # print("%{} is done".format(y/10))
        #     image_y = y0 + y * y_pixel
        #
        #     # for each row
        #     for x in range(self.width):
        #         image_x = x0 + x * x_pixel
        #         ray = Ray(origin=self.camera.camPosition, direction=Point3f(image_x, image_y, 1) - self.camera.camPosition)
        #         clr = self.trace(ray, scene)
        #         self.data[y][x] = [to_byte(clr.r), to_byte(clr.g), to_byte(clr.b)]

    def writeTo(self, name='output.png'):
        img = Image.fromarray(self.data, 'RGB')
        img.save(name)
        Image.open(name).show()

    def trace(self, ray, scene):
        """
        Traces the ray in given scene
        :param ray: Shot from camera to pixel position
        :param scene: spheres
        :return: Color of the pixel (Currently in grayscale)
        """
        # how many times rays can bounce
        depth = 2
        # background color
        color = ColorRGBA(0.1, 0.1, 0.1, 0)
        # Find the nearest object hit by the ray in the scene
        dist_hit, obj_hit = self.findNearest(ray, scene)
        if obj_hit is None:
            return color
        elif obj_hit.type == "light":
            return ColorRGBA(1, 1, 1, 1)
        color = obj_hit.color
        hit_pos = ray.origin + ray.direction * dist_hit

        normal = hit_pos - obj_hit.position
        normal = normal.normalize()
        hit_pos = hit_pos + normal * 0.0001

        shadow = self.traceToLight(hit_pos, scene)
        if shadow is None:
            return ColorRGBA(0.0, 0.0, 0.0, 0)
        # if obj_hit.radius > 100:
        #     print(hit_pos)
        #     if int(hit_pos.x) % 2 == 1 and  int(hit_pos.z) % 2 == 1:
        #         return ColorRGBA(0, 0.3, 0.4, 1)

        if obj_hit.material == "diffuse":
            NdotL = normal.dot(shadow.direction.normalize())
            return color * NdotL
        elif obj_hit.material == "transparent":
            return self.traceReflection(ray, scene, 3)

        # if obj_hit.material == "transparent":
        #     return ColorRGBA(1, 1, 1, 1)

        return color

    def traceReflection(self, ray, scene, depth):
        color = ColorRGBA(0, 0, 0, 0)
        if depth == 0:
            return color
        dist_hit, obj_hit = self.findNearest(ray, scene)

        if obj_hit is None:
            return color
        elif obj_hit.type == "light":
            return ColorRGBA(1, 1, 1, 1)
        elif obj_hit.material == "diffuse":
            color = obj_hit.color
            hit_pos = ray.origin + ray.direction * dist_hit

            normal = hit_pos - obj_hit.position
            normal = normal.normalize()
            hit_pos = hit_pos + normal * 0.0001

            shadow = self.traceToLight(hit_pos, scene)
            if shadow is None:
                return ColorRGBA(0.0, 0.0, 0.0, 0)

            if obj_hit.material == "diffuse":
                NdotL = normal.dot(shadow.direction.normalize())
                return color * NdotL

        else:
            hit_pos = ray.origin + ray.direction * dist_hit
            normal = hit_pos - obj_hit.position
            normal = normal.normalize()
            hit_pos = hit_pos + normal * 0.0001
            reflection = Ray(origin=hit_pos,
                             direction=ray.direction.reflect(normal))
            return color + self.traceReflection(reflection, scene, depth-1)

    def traceRefraction(self, ray, scene, depth):
        color = ColorRGBA(0, 0, 0, 0)
        if depth == 0:
            return color
        dist_hit, obj_hit = self.findNearest(ray, scene)

        if obj_hit is None:
            return color
        elif obj_hit.type == "light":
            return ColorRGBA(1, 1, 1, 1)
        elif obj_hit.material == "diffuse":
            color = obj_hit.color
            hit_pos = ray.origin + ray.direction * dist_hit

            normal = hit_pos - obj_hit.position
            normal = normal.normalize()
            hit_pos = hit_pos + normal * 0.0001

            shadow = self.traceToLight(hit_pos, scene)
            if shadow is None:
                return ColorRGBA(0.0, 0.0, 0.0, 0)

            if obj_hit.material == "diffuse":
                NdotL = normal.dot(shadow.direction.normalize())
                return color * NdotL

        else:
            hit_pos = ray.origin + ray.direction * dist_hit
            normal = hit_pos - obj_hit.position
            normal = normal.normalize()
            hit_pos = hit_pos + normal * 0.0001
            refr = ray.direction.refract(normal, 1.5)
            if refr == 0:
                return ColorRGBA(0, 0, 0, 0)
            refraction = Ray(origin=hit_pos,
                             direction=refr)
            return color + self.traceRefraction(refraction, scene, depth - 1)

    @staticmethod
    def findNearest(ray, scene):
        """
        Finds the nearest object and the point ray is hitting.
        :param ray:  Could be reflection or camera itself
        :param scene: -
        :return: Minimum distance of the point hit by ray, the object itself hit by ray
        """
        minDistance = None
        objHit = None
        for obj in scene.objects:
            dist = obj.intersect(ray)
            if dist is not None and (objHit is None or dist < minDistance):
                minDistance = dist
                objHit = obj

        return minDistance, objHit

    @staticmethod
    def isHittingSomething(ray, scene):
        """
        Implemented for optimisation, since for ambient occlusion closest point is not necessary, just knowing if the
        ray is hitting something is enough for AO.
        :param ray: -
        :param scene: -
        :return: Bool
        """
        for node in scene.objects:
            dist = node.intersect(ray)
            if dist is not None:
                return True

        return False

    def traceToLight(self, point, scene):
        minDistance = None
        objHit = None
        rayHit = None
        for light in scene.lights:

            ray = Ray(origin=point,
                      direction=(light.position - point))
            for obj in scene.objects:
                dist = obj.intersect(ray)
                if dist is not None and (objHit is None or dist < minDistance):
                    if obj.material == "transparent":
                        continue
                    minDistance = dist
                    objHit = obj
                    rayHit = ray
        if objHit.type != "light":
            return None

        return rayHit

        # for light in scene.lights:
        #     ray = Ray(origin=point,
        #               direction=(light.position - point))
        #     dist_hit, obj_hit = self.findNearest(ray, scene)
        #     if obj_hit is not None:
        #         if obj_hit.type == "light":
        #             return ray.direction
        # return False

    def ambient(self, normal, scene):
        """
        Shooting Rays that are aligned to the normal. And finds the percentage of rays hitting at least one object.

        :param normal: Ray originated from hit point, directing hit_point - sphere_center
        :param scene:-
        :return: Returns ambient intensity of the point
        """
        light_intensity = 0

        normalDir = normal.direction
        # coordinate system with our normal is Y axis, soon to be used to rotate samples
        Nt, Nb = self.createCoordSystem(normal)

        for _ in range(self.SAMPLE_COUNT):

            u1 = random.uniform(0, 1)
            u2 = random.uniform(0, 1)

            sinTheta = math.sqrt(1 - u1 * u1)
            phi = 2 * math.pi * u2
            x = sinTheta * math.cos(phi)
            z = sinTheta * math.sin(phi)
            y = u1

            # r = math.sqrt(u1)
            # theta = 2 * math.pi * u2
            # x = r * math.cos(theta)
            # z = r * math.sin(theta)
            # y = math.sqrt(max(0.0, 1-u1))

            # deleted for optimization
            # vec = Vector3f(x, y, z)
            # rotating the sample to the hemisphere
            sample = Vector3f(
                x * Nb.x + y * normalDir.x + z * Nt.x,
                x * Nb.y + y * normalDir.y + z * Nt.y,
                x * Nb.z + y * normalDir.z + z * Nt.z
            )

            sampleRay = Ray(origin=normal.origin,
                            direction=sample)
            isHitting = self.isHittingSomething(sampleRay, scene)
            # if sample hits any object
            if isHitting is True:
                light_intensity += 1

        return self.SAMPLE_COUNT - light_intensity

    @staticmethod
    def createCoordSystem(normal):
        """
        Calculates the x, y, z axes of points space.
        :param normal:
        :return:
        """
        normalDir = normal.direction
        if abs(normalDir.x) > abs(normalDir.y):
            Nt = Vector3f(normalDir.z, 0, -normalDir.x) / \
                 math.sqrt(normalDir.x * normalDir.x + normalDir.z * normalDir.z)
        else:
            Nt = Vector3f(0, -normalDir.z, normalDir.y) / \
                 math.sqrt(normalDir.y * normalDir.y + normalDir.z * normalDir.z)

        Nb = normalDir.cross(Nt)

        return Nt, Nb

    def createSamples(self):
        """

        :return:
        """
        for i in range(self.SAMPLE_COUNT):
            u1 = random.uniform(0, 1)
            u2 = random.uniform(0, 1)

            sinTheta = math.sqrt(1 - u1 * u1)
            phi = 2 * math.pi * u2
            x = sinTheta * cos(phi)
            z = sinTheta * sin(phi)
            vec = Vector3f(x, u1, z)
            self.samples.append(vec)

    def generateUniform(self):
        for i in range(self.SAMPLE_COUNT * 2):
            u1 = random.uniform(0, 1)
            u2 = random.uniform(0, 1)

            self.uniforms.append(u1)
            self.uniforms.append(u2)
