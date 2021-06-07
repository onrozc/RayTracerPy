# CENG 488 Assignment2 by
# Onur Ozcan
# StudentId:240201032
# 5 2021
# This file is based on the template code given in CENG487
import copy
from math import sqrt, acos

__all__ = ['HCoord', 'Vector3f', 'Point3f', 'ColorRGBA']


class HCoord:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def x(self):
        return self.x

    def y(self):
        return self.y

    def z(self):
        return self.z

    def sqrlen(self):
        return 1.0 * self.x * self.x + self.y * self.y + self.z * self.z + 0

    def len(self):
        return sqrt(self.sqrlen())

    def dot(self, other):
        return 1.0 * other.x * self.x + other.y * self.y + other.z * self.z

    def cross(self, other):
        return HCoord(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x,
                      self.w)

    def cosa(self, other):
        return min(self.dot(other) / (self.len() * other.len()), 1.0)

    def angle(self, other):
        return acos(self.cosa(other))

    def normalize(self):
        l = self.len()
        return HCoord(self.x / l, self.y / l, self.z / l, 0)

    def project(self, other):

        return other.normalize() * (self.len() * self.cosa(other))

    def reflect(self, normal):
        # B = self.project(normal.normalize())
        #
        # A = self - self.cosa(normal) * normal
        #
        # R = A.normalize() - B.normalize()

        return self - 2 * (normal.dot(self)) * normal

    def refract(self, normal, ior):
        cos = self.cosa(normal)
        Ncopy = copy.deepcopy(normal)
        NdotI = Ncopy.dot(self)
        etai = 1
        etat = ior
        if NdotI < 0:
            NdotI = -NdotI
        else:
            Ncopy = Vector3f(0, 0, 0)-Ncopy
            etai, etat = etat, etai
        eta = etai / etat
        k = 1 - eta * eta * (1 - cos * cos)
        if k < 0:
            return 0
        else:
            return eta * self + (eta * NdotI - sqrt(k)) * Ncopy



    # def Rx(self, x):
    #     m = Matrix.create([1, 0, 0, 0, 0, cos(x), -sin(x), 0, 0, sin(x), cos(x), 0, 0, 0, 0, 1])
    #     return m.vecmul(self)
    #
    # def Ry(self, x):
    #     m = Matrix.create([cos(x), 0, sin(x), 0, 0, 1, 0, 0, -sin(x), 0, cos(x), 0, 0, 0, 0, 1])
    #     return m.vecmul(self)
    #
    # def Rz(self, x):
    #     m = Matrix.create([cos(x), -sin(x), 0, 0, sin(x), cos(x), 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    #     return m.vecmul(self)
    #
    # def S(self, scalar):
    #     return self * scalar
    #
    # def T(self, x, y, z):
    #     m = Matrix.create([1, 0, 0, x, 0, 1, 0, y, 0, 0, 1, z, 0, 0, 0, 1])
    #     return m.vecmul(self)

    def __add__(self, other):

        x = 1.0 * self.x + other.x
        y = 1.0 * self.y + other.y
        z = 1.0 * self.z + other.z
        # w = 1.0 * self.w + other.w
        return HCoord(x, y, z, 0)

    def __sub__(self, other):
        return Vector3f(self.x - other.x,
                        self.y - other.y,
                        self.z - other.z)

    def __truediv__(self, scalar):
        if (scalar == 0):
            return self
        else:
            return HCoord(self.x / scalar, self.y / scalar, self.z / scalar, self.w / scalar)

    def __mul__(self, scalar):
        return HCoord(scalar * self.x, scalar * self.y, scalar * self.z, self.w * scalar)

    def __rmul__(self, scalar):
        return HCoord(scalar * self.x, scalar * self.y, scalar * self.z, self.w * scalar)

    def __str__(self):
        return "(" + str(self.x) + " " + str(self.y) + " " + str(self.z) + " " + str(self.w) + ")"

    def __repr__(self):
        return self.__str__()


class Vector3f(HCoord):
    def __init__(self, x, y, z):
        HCoord.__init__(self, x, y, z, 0)


class Point3f(HCoord):
    def __init__(self, x, y, z):
        HCoord.__init__(self, x, y, z, 1.0)

    def __sub__(self, other):
        return Vector3f(self.x - other.x,
                        self.y - other.y,
                        self.z - other.z)

    def __add__(self, other):
        return Point3f( self.x + other.x,
                            self.y + other.y,
                            self.z + other.z )


class ColorRGBA(HCoord):
    def __init__(self, r, g, b, a):
        HCoord.__init__(self, r, g, b, a)
        self.r = self.x
        self.g = self.y
        self.b = self.z
        self.a = self.w

    def __mul__(self, scalar):
        return ColorRGBA(scalar * self.r, scalar * self.g, scalar * self.b, self.a * scalar)

    def __truediv__(self, scalar):

        if scalar == 0:
            return self
        else:
            return ColorRGBA(self.r / scalar, self.g / scalar, self.b / scalar, self.a / scalar)

    def __add__(self, other):

        r = 1.0 * self.r + other.r
        g = 1.0 * self.g + other.g
        b = 1.0 * self.b + other.b
        # w = 1.0 * self.w + other.w
        return ColorRGBA(r, g, b, 0)

# /
#
# from math import sin, cos, sqrt, acos
#
# import numpy
#
# __all__ = ['HCoord', 'Vector3f', 'Point3f', 'ColorRGBA']
#
#
# class HCoord:
#     def __init__(self, a):
#         self.na = a
#
#     def from4d(self, x, y, z, w):
#         self.na = numpy.array([x, y, z, w], dtype='float32')
#
#     def x(self):
#         return self.na[0]
#
#     def asNumpy(self):
#         return self.na
#
#     def y(self):
#         return self.na[1]
#
#     def z(self):
#         return self.na[2]
#
#     def w(self):
#         return self.na[3]
#
#     def sqrlen(self):
#         return 1.0 * numpy.dot(self.na, self.na)
#
#     def len(self):
#         return sqrt(self.sqrlen())
#
#     def dot(self, other):
#         return 1.0 * numpy.dot(other.na, self.na)
#
#     def cross(self, other):
#         result = numpy.cross(self.na[0:3], other.na[0:3], axisa=0, axisb=0, axisc=0)
#         return Vector3f(result[0], result[1], result[2])
#
#     def cosa(self, other):
#         return min(max(self.dot(other) / (self.len() * other.len()), 0.0), 1.0)
#
#     def angle(self, other):
#         return acos(self.cosa(other))
#
#     def normalize(self):
#         vecLen = self.len()
#         self.na = self.na / vecLen
#         return self
#
#     def project(self, other):
#         return other.normalize() * (self.len() * self.cosa(other))
#
#     def Rx(self, x):
#         import matrix
#         m = matrix.Matrix.create([1, 0, 0, 0, 0, cos(x), -sin(x), 0, 0, sin(x), cos(x), 0, 0, 0, 0, 1])
#         return m.vecmul(self)
#
#     def Ry(self, x):
#         import matrix
#         m = matrix.Matrix.create([cos(x), 0, sin(x), 0, 0, 1, 0, 0, -sin(x), 0, cos(x), 0, 0, 0, 0, 1])
#         return m.vecmul(self)
#
#     def Rz(self, x):
#         import matrix
#         m = matrix.Matrix.create([cos(x), -sin(x), 0, 0,
#                                   sin(x), cos(x), 0, 0,
#                                   0, 0, 1, 0,
#                                   0, 0, 0, 1])
#         return m.vecmul(self)
#
#     def Ru(self, x, u):
#         import matrix
#         m = matrix.Matrix.create([numpy.cos(x) + (u.x() ** 2) * (1 - numpy.cos(x)), u.x() * u.y() * (1 - numpy.cos(x)) - u.z() * numpy.sin(x),
#                                   u.x() * u.z() * (1 - numpy.cos(x)) + u.y() * numpy.sin(x),
#                                   0,
#                                   u.x() * u.y() * (1 - numpy.cos(x)) + u.z() * numpy.sin(x), numpy.cos(x) + (u.y() ** 2) * (1 - numpy.cos(x)),
#                                   u.y() * u.z() * (1 - numpy.cos(x)) - u.x() * numpy.sin(x),
#                                   0,
#                                   u.x() * u.z() * (1 - numpy.cos(x)) - u.y() * numpy.sin(x),
#                                   u.y() * u.z() * (1 - numpy.cos(x)) + u.x() * numpy.sin(x),
#                                   numpy.cos(x) + (u.z() ** 2) * (1 - numpy.cos(x)),
#                                   0,
#                                   0, 0, 0, 1])
#         return m.vecmul(self)
#
#     def S(self, x, y, z):
#         import matrix
#         m = matrix.Matrix.create([x, 0, 0, 0, 0, y, 0, 0, 0, 0, z, 0, 0, 0, 0, 1])
#         return m.vecmul(self)
#
#     def T(self, x, y, z):
#         import matrix
#         m = matrix.Matrix.create([1, 0, 0, x,
#                                   0, 1, 0, y,
#                                   0, 0, 1, z,
#                                   0, 0, 0, 1])
#         return m.pointmul(self)
#
#     def __add__(self, other):
#         self.na = self.na + other.na
#         return self
#
#     def __sub__(self, other):
#
#         self.na = self.na - other.na
#         return self
#
#     def __truediv__(self, scalar):
#         if (scalar == 0):
#             return self
#         else:
#             self.na = self.na / scalar
#             return self
#
#     def __mul__(self, scalar):
#
#         na = scalar * self.na
#         return Point3f (na[0], na[1], na[2])
#
#     def __rmul__(self, scalar):
#         self.na = scalar * self.na
#         return self
#
#     def __str__(self):
#         return "(" + str(self.x()) + " " + str(self.y()) + " " + str(self.z()) + " " + str(self.w()) + ")"
#
#     def __repr__(self):
#         return self.__str__()
#
#
# class Vector3f(HCoord):
#     def __init__(self, x, y, z):
#         self.from4d(x, y, z, 0.0)
#     def __sub__(self, other):
#         result = self.na - other.na
#         return Vector3f(result[0], result[1], result[2])
#
#     def __add__(self, other):
#         result = self.na + other.na
#         return Point3f(result[0], result[1], result[2])
#
#     def fromNumpy(self, na):
#         self.na = na
#
#
# class Point3f(HCoord):
#     def __init__(self, x, y, z):
#         self.from4d(x, y, z, 1.0)
#
#     def __sub__(self, other):
#         result = self.na - other.na
#         return Vector3f(result[0], result[1], result[2])
#
#     def __add__(self, other):
#         result = self.na + other.na
#         return Point3f(result[0], result[1], result[2])
#
#
# class ColorRGBA(HCoord):
#     def __init__(self, r, g, b, a):
#         self.from4d(r, g, b, a)
#
#     def __add__(self, other):
#         self.na = self.na + other.na
#         return self
#
#     def r(self):
#         return self.na[0]
#
#     def g(self):
#         return self.na[1]
#
#     def b(self):
#         return self.na[2]
#
#     def a(self):
#         return self.na[3]
