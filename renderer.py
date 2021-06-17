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

        ray = Ray(origin=self.camera.camPosition, direction=Point3f(image_x, image_y, 0) - self.camera.camPosition)
        clr = self.trace(ray, scene)
        return to_byte(clr.r), to_byte(clr.g), to_byte(clr.b)

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
        # if ray hits nothing return Background color
        if obj_hit is None:
            return color
        # if ray hits light we will return lights color. In this case light is white
        elif obj_hit.type == "light":
            return obj_hit.color

        # so if we reached here it means we are hitting an object in the screen, so what is it? Is it matte(diffuse),
        # or is it transparent like glass or water. Or is it mirror.
        # Each object has their color (fixed for now)
        color = obj_hit.color
        # exact point of the intersection of ray and sphere
        hit_pos = ray.origin + ray.direction * dist_hit
        # normal at the hit position
        normal = hit_pos - obj_hit.position
        normal = normal.normalize()
        # due to our finite memory there will be numeric errors. So ving the hit position out a little fixes those.
        hit_pos = hit_pos + normal * 0.0001

        # This is either none or A ray to a light but it must return list of lights, not a single light hit status.
        # return self.phongShader(eye_ray=ray, normal_ray=Ray(hit_pos, normal),
        #                         obj_color=obj_hit.color, scene=scene)
        # TODO: Return multiple lights
        # shadow = self.traceToLight(hit_pos, scene)
        # this means the point is not seeing any light hence it is shadow.
        # TODO: Ambient Occlusion
        # if shadow is None:
        #     return self.ambient(Ray(hit_pos, normal), scene, obj_hit.color) * 0.15
        # else:
        #     ambientStr = 0.15
        #     ambient = self.ambient(Ray(hit_pos, normal), scene, obj_hit.color) * ambientStr

            # return ColorRGBA(0.0, 0.0, 0.0, 0)
        # if obj_hit.radius > 100:
        #     print(hit_pos)
        #     if int(hit_pos.x) % 2 == 1 and  int(hit_pos.z) % 2 == 1:
        #         return ColorRGBA(0, 0.3, 0.4, 1)
        # If the object is matte calculate the diffuse and specular lights of the fragment
        if obj_hit.material == "diffuse":
            return self.phongShader(eye_ray=ray, normal_ray=Ray(hit_pos, normal),
                                    obj_color=obj_hit.color, scene=scene)


        # If the object is transparent there will be two rays:
        #   1) Reflection
        #   2) Refraction
        # And we need to combine those two for sake of Newton. Fresnel equations come in handy for that.
        elif obj_hit.material == "transparent":
            fresnel = self.fresnel(ray.direction, normal, 1.3)
            return (self.traceReflection(ray, scene, 6) * fresnel + self.traceRefraction(ray, scene, 6)) * (
                    1 - fresnel)

        # if obj_hit.material == "transparent":
        #     return ColorRGBA(1, 1, 1, 1)

        return color

    def traceReflection(self, ray, scene, depth):
        color = ColorRGBA(0.1, 0.1, 0.1, 0)
        if depth == 0:
            return color
        dist_hit, obj_hit = self.findNearest(ray, scene)

        if obj_hit is None:
            return color
        elif obj_hit.type == "light":
            return ColorRGBA(1, 1, 1, 1)
        elif obj_hit.material == "diffuse":
            hit_pos = ray.origin + ray.direction * dist_hit
            normal = hit_pos - obj_hit.position
            normal = normal.normalize()
            hit_pos = hit_pos + normal * 0.0001
            return self.phongShader(eye_ray=ray, normal_ray=Ray(hit_pos, normal),
                                    obj_color=obj_hit.color, scene=scene)
            # shadow = self.traceToLight(hit_pos, scene)
            # if shadow is None:
            #     return ColorRGBA(0.0, 0.0, 0.0, 0)
            #
            # if obj_hit.material == "diffuse":
            #     NdotL = normal.dot(shadow.direction.normalize())
            #
            #     # specular part
            #     specStr = 0.3
            #     reflectDir = shadow.direction.normalize().reflect(normal)
            #     spec = math.pow(max(reflectDir.dot(ray.direction), 0.0), 16)
            #     specular = specStr * spec
            #
            #     return color * (specular + NdotL)

        else:
            hit_pos = ray.origin + ray.direction * dist_hit
            normal = hit_pos - obj_hit.position
            normal = normal.normalize()
            hit_pos = hit_pos + normal * 0.0001
            reflection = Ray(origin=hit_pos,
                             direction=ray.direction.reflect(normal))
            return color + self.traceReflection(reflection, scene, depth - 1)

    def traceRefraction(self, ray, scene, depth):
        color = ColorRGBA(0.1, 0.1, 0.1, 0)
        if depth == 0:
            return color
        dist_hit, obj_hit = self.findNearest(ray, scene)

        if obj_hit is None:
            return color
        elif obj_hit.type == "light":
            return ColorRGBA(1, 1, 1, 1)
        elif obj_hit.material == "diffuse":
            hit_pos = ray.origin + ray.direction * dist_hit
            normal = hit_pos - obj_hit.position
            normal = normal.normalize()
            hit_pos = hit_pos + normal * 0.0001
            return self.phongShader(eye_ray=ray, normal_ray=Ray(hit_pos, normal),
                                    obj_color=obj_hit.color, scene=scene)

        else:
            hit_pos = ray.origin + ray.direction * dist_hit
            normal = hit_pos - obj_hit.position
            normal = normal.normalize()
            NdotL = normal.dot(ray.direction)
            hit_pos = hit_pos - normal * 0.0001
            if NdotL <= 0:
                refr = ray.direction.refract(normal, 1.3)
            else:
                refr = ray.direction.refract(normal, 1)
            if refr == 0:
                internalReflection = Ray(origin=hit_pos,
                                         direction=ray.direction.reflect(-normal))
                color + self.traceReflection(internalReflection, scene, depth - 1)
            refraction = Ray(origin=hit_pos,
                             direction=refr)
            return color + self.traceRefraction(refraction, scene, depth - 1)

    def phongShader(self, eye_ray, normal_ray, obj_color, scene):
        ambient_strength = 0.15
        diffuse_strength = 0.6
        specular_strength = 0.25
        total_diffuse = ColorRGBA(0, 0, 0, 1)
        total_specular = ColorRGBA(0, 0, 0, 1)
        ambient = self.ambient(normal_ray, scene, obj_color) * ambient_strength
        # ambient = ColorRGBA(0, 0, 0, 1)
        for light in scene.lights:
            ray = Ray(origin=normal_ray.origin,
                      direction=(light.position - normal_ray.origin))
            _, obj_hit = self.traceToLight(ray, scene)
            if obj_hit is light:
                # great we do hit this light
                # diffuse part
                n_dot_l = ray.direction.dot(normal_ray.direction)
                total_diffuse += obj_color * n_dot_l * diffuse_strength

                # specular part... fuck i need view position for this and I don't really wanna have 5 arguments.

                reflect_dir = ray.direction.normalize().reflect(normal_ray.direction.normalize())
                spec = math.pow(max(reflect_dir.normalize().dot(eye_ray.direction.normalize()), 0.0), 16)
                specular = specular_strength * spec
                total_specular += obj_color * specular

            # TODO: maybe ambient can use specific color from dome light.

        return ambient + (total_specular + total_diffuse) / 2

    @staticmethod
    def specularColor(L, N, R, Intensity):
        pass

    @staticmethod
    def fresnel(ray, normal, ior):
        angle = ray.cosa(normal)
        etai = 1
        etat = ior
        if angle > 0:
            etai, etat = etat, etai

        sint = etai / etat * math.sqrt(max(0.0, 1 - angle * angle))
        if sint >= 1:
            return 1
        else:
            cost = math.sqrt(max(0.0, 1 - sint * sint))
            angle = abs(angle)
            Rs = ((etat * angle) - (etai * cost)) / ((etat * angle) + (etai * cost))
            Rp = ((etai * angle) - (etat * cost)) / ((etai * angle) + (etat * cost))
            return (Rs * Rs + Rp * Rp) / 2

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

    def traceToLight(self, ray, scene):
        """
        Currently Works only for one light
        :param point:
        :param scene:
        :return:
        minDistance = None
        objHit = None
        for obj in scene.objects:
            dist = obj.intersect(ray)
            if dist is not None and (objHit is None or dist < minDistance):
                minDistance = dist
                objHit = obj

        return minDistance, objHit
        """
        minDistance = None
        objHit = None
        for obj in scene.objects:
            dist = obj.intersect(ray)
            if dist is not None and (objHit is None or dist < minDistance):
                if obj.material == "transparent":
                    continue
                minDistance = dist
                objHit = obj

        return minDistance, objHit

    def ambient(self, normal, scene, objColor):
        """
        Shooting Rays that are aligned to the normal. And finds the percentage of rays hitting at least one object.

        :param objColor:
        :param normal: Ray originated from hit point, directing hit_point - sphere_center
        :param scene:-
        :return: Returns ambient intensity of the point
        """
        light_intensity = 0
        color = ColorRGBA(0.0, 0.0, 0.0, 0)
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
            # _, nearestObj = self.findNearest(sampleRay, scene)
            # if nearestObj is not None:
            #     color += nearestObj.color

            isHitting = self.isHittingSomething(sampleRay, scene)
            if isHitting is False:
                color += objColor
            # if sample hits any object
            # if isHitting is True:
            #     light_intensity += 1
        return color / self.SAMPLE_COUNT
        # return self.SAMPLE_COUNT - light_intensity

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
