# CENG 488 Assignment2 by
# Onur Ozcan
# StudentId:240201032
# 5 2021

class Ray:
    def __init__(self, origin, direction):
        self.direction = direction.normalize()
        self.origin = origin

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value.normalize()

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value


class Reflection(Ray):
    def __init__(self, origin, direction):
        super().__init__(origin, direction)


class Refraction(Ray):
    def __init__(self, origin, direction):
        super().__init__(origin, direction)
