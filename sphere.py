# CENG 488 Assignment2 by
# Onur Ozcan
# StudentId:240201032
# 5 2021

import math
import random

from vector import *


class Sphere:
    @staticmethod
    def load(prop, sType="object"):
        try:
            pos = prop["position"]
            return Sphere(radius=prop["radius"],
                          position=Point3f(pos[0], pos[1], pos[2]),
                          color=ColorRGBA(random.uniform(0, 1),
                                          random.uniform(0, 1),
                                          random.uniform(0, 1), 1),
                          sType=sType)
        except ValueError:
            raise Exception("Parsing Error!")

    def __init__(self, radius=0, position=Point3f(0, 0, 0), color=ColorRGBA(0.8, 0.8, 0.8, 1), sType="object",
                 material="diffuse"):
        """

        :param radius: radius of the sphere
        :param position: origin of the sphere
        :param color: color of the sphere
        """
        self.radius = radius
        self.position = position
        self.color = color
        self.type = sType
        self.material = material

    @property
    def material(self) -> str:
        return self._material

    @material.setter
    def material(self, value: str):
        self._material = value

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float):
        self._radius = value

    @property
    def position(self) -> Point3f:
        return self._position

    @position.setter
    def position(self, value: Point3f):
        self._position = value

    @property
    def color(self) -> ColorRGBA:
        return self._color

    @color.setter
    def color(self, value: ColorRGBA):
        self._color = value

    def intersect(self, ray):
        """Checks if ray intersects this sphere. Returns distance to intersection or None if there is no intersection"""
        sphere_to_ray = ray.origin - self.position
        # a = 1
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - self.radius * self.radius
        discriminant = b * b - 4 * c

        if discriminant >= 0:
            dist = (-b - math.sqrt(discriminant)) / 2
            if dist > 0:
                return dist
        return None



class Light(Sphere):
    def __init__(self, intensity=0):
        super().__init__()
        self.intensity = intensity

    @property
    def intensity(self) -> float:
        return self.intensity

    @intensity.setter
    def intensity(self, value: float):
        self.intensity = value
