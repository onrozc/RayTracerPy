# CENG 488 Assignment 8 by
# Onur Ozcan
# StudentId:240201032
# 6 2021
from matrix import Matrix
from vector import *


class Camera(object):
    def __init__(self, camPos=Vector3f(0, 0, 0)):
        self.camPosition = camPos
        self.camCenter = Point3f(0.0, 0.0, 0.0)

    def getModelMatrix(self, objectPosition):

        m = Matrix.create([1.0, 0.0, 0.0, objectPosition[0],
                           0.0, 1.0, 0.0, objectPosition[1],
                           0.0, 0.0, 1.0, objectPosition[2],
                           0, 0, 0, 1.0])
        return m.asNumpy()
    #     self.camUpAxis = Vector3f(0.0, 1.0, 0.0)
    #     self.camTranslation = Point3f(0.0, 0.0, 0.0)
    #     self.camNear = 1
    #     self.camFar = 100.0
    #     self.camAspect = 1
    #     self.camFov = 45.0
    #     self.isMoving = True
    #     self.turn = 0
    #     self.cameraSpeed = 0.02
    #     self.pitch = 0
    #     self.yaw = 0
    #     self.camZAxis = self.camCenter - self.camPosition
    #     self.camZAxis = self.camZAxis.normalize()
    #     self.camXAxis = self.camZAxis.cross(self.camUpAxis)
    #     self.camYAxis = self.camXAxis.cross(self.camZAxis)
    #
    # def setCenter(self, center):
    #     self.camCenter = center
    #
    # def setPosition(self, pos):
    #     self.camPosition = pos
    #
    # def setFov(self, fov):
    #     self.camFov = fov
    #
    # def setAspect(self, w, h):
    #     if h != 0:
    #         self.camAspect = w / h
    #
    # def updateCamAxes(self):
    #     self.camZAxis = self.camCenter - self.camPosition
    #     self.camZAxis = self.camZAxis.normalize()
    #     self.camXAxis = self.camZAxis.cross(self.camUpAxis)
    #     self.camYAxis = self.camXAxis.cross(self.camZAxis)
    #
    # def turnCameraAxes(self, xAngle, yAngle, vec):
    #     self.camXAxis = self.camXAxis.Ry(xAngle)
    #     self.camYAxis = self.camYAxis.Ry(xAngle)
    #     self.camZAxis = self.camZAxis.Ry(xAngle)
    #
    #     self.camXAxis = self.camXAxis.Ru(yAngle, vec)
    #     self.camYAxis = self.camYAxis.Ru(yAngle, vec)
    #     self.camZAxis = self.camZAxis.Ru(yAngle, vec)
    #
    # def getProjMatrix(self):
    #     f = numpy.reciprocal(numpy.tan(numpy.divide(numpy.deg2rad(self.camFov), 2.0)))
    #     base = self.camNear - self.camFar
    #     term_0_0 = numpy.divide(f, self.camAspect)
    #     term_2_2 = numpy.divide(self.camFar + self.camNear, base)
    #     term_2_3 = numpy.divide(numpy.multiply(numpy.multiply(2, self.camNear), self.camFar), base)
    #
    #     # https://en.wikibooks.org/wiki/GLSL_Programming/Vertex_Transformations
    #     return numpy.array([term_0_0, 0.0, 0.0, 0.0,
    #                         0.0, f, 0.0, 0.0,
    #                         0.0, 0.0, term_2_2, -1,
    #                         0.0, 0.0, term_2_3, 0.0], dtype='float32')
    #
    # def zoom(self, direction):
    #     eye = self.camCenter - self.camPosition
    #     size = eye.len()
    #     size /= 100
    #
    #     eye.normalize()
    #     eye = eye.S(size, size, size)
    #     if direction:
    #         self.camPosition = self.camPosition.T(eye.x(), eye.y(), eye.z())
    #     else:
    #         self.camPosition = self.camPosition.T(-eye.x(), -eye.y(), -eye.z())
    #
    # def resetCamera(self):
    #     self.camPosition = Vector3f(5, 5, 5)
    #     self.camCenter = Vector3f(0.0, 0.0, 0.0)
    #     self.camUpAxis = Vector3f(0.0, 1.0, 0.0)
    #     self.camTranslation = Point3f(0.0, 0.0, 0.0)
    #     self.updateCamAxes()
    #
    # def moveInZaxis(self, direction):
    #     direction = direction * 10
    #     camZAxis = self.camCenter - self.camPosition
    #     camZAxis = camZAxis.normalize()
    #     camXAxis = camZAxis.cross(self.camUpAxis)
    #
    #     camYAxis = camXAxis.cross(camZAxis)
    #
    #     self.camPosition = self.camPosition.T(camZAxis.x() * direction, camZAxis.y() * direction,
    #                                           camZAxis.z() * direction)
    #     self.camCenter = self.camCenter.T(camZAxis.x() * direction, camZAxis.y() * direction, camZAxis.z() * direction)
    #     self.camTranslation = self.camTranslation.T(camZAxis.x() * direction, camZAxis.y() * direction,
    #                                                 camZAxis.z() * direction)
    #
    # def pan(self, x, y):
    #     s = 1 / 10
    #     # camZAxis = self.camCenter - self.camPosition
    #     # camZAxis = camZAxis.normalize()
    #     # camXAxis = camZAxis.cross(self.camUpAxis)
    #     #
    #     # camYAxis = camXAxis.cross(camZAxis)
    #
    #     self.camPosition = self.camPosition.T(self.camYAxis.x() * y, self.camYAxis.y() * y, self.camYAxis.z() * y)
    #     self.camCenter = self.camCenter.T(self.camYAxis.x() * y, self.camYAxis.y() * y, self.camYAxis.z() * y)
    #     self.camTranslation = self.camTranslation.T(self.camYAxis.x() * y, self.camYAxis.y() * y, self.camYAxis.z() * y)
    #
    #     self.camPosition = self.camPosition.T(self.camXAxis.x() * x, self.camXAxis.y() * x, self.camXAxis.z() * x)
    #     self.camCenter = self.camCenter.T(self.camXAxis.x() * x, self.camXAxis.y() * x, self.camXAxis.z() * x)
    #     self.camTranslation = self.camTranslation.T(self.camXAxis.x() * x, self.camXAxis.y() * x, self.camXAxis.z() * x)
    #
    # def arcball(self, xAngle, yAngle):
    #     z = self.camCenter - self.camPosition
    #     z = z.normalize()
    #     x = z.cross(self.camUpAxis)
    #     self.camPosition = self.camPosition.Ru(yAngle, x)
    #     self.camPosition = self.camPosition.Ry(xAngle)
    #
    #     # self.camUpAxis = self.camUpAxis.normalize()
    #
    #     self.turnCameraAxes(xAngle, yAngle, x)
    #
    # def rotateLR(self, angle):
    #     """
    #     Turns the camera around the global Y axis
    #     :param angle:
    #     :return:
    #     """
    #     # camZAxis = self.camCenter - self.camPosition
    #     # camZAxis = camZAxis.normalize()
    #     #
    #     # camXAxis = camZAxis.cross(self.camUpAxis)
    #     self.camPosition = self.camPosition.T(self.camTranslation.x(), self.camTranslation.y(),
    #                                           self.camTranslation.z())
    #
    #     self.camPosition = self.camPosition.Ry(angle)
    #     self.camUpAxis = self.camUpAxis.Ry(angle)
    #     self.camUpAxis = self.camUpAxis.normalize()
    #
    #     self.camPosition = self.camPosition.T(-self.camTranslation.x(), -self.camTranslation.y(),
    #                                           -self.camTranslation.z())
    #     self.updateCamAxes()
    #
    # def rotateUD(self, angle):
    #
    #     """
    #     Turns the camera around the camera X axis
    #     :param angle:
    #     :return:
    #     """
    #
    #     self.camPosition = self.camPosition.Ru(angle, self.camXAxis)
    #     self.camUpAxis = self.camUpAxis.Ru(angle, self.camXAxis)
    #     self.camUpAxis = self.camUpAxis.normalize()
    #     # self.camPosition = self.camPosition.T(-self.camTranslation.x(), -self.camTranslation.y(),
    #     #                                       -self.camTranslation.z())
    #     self.updateCamAxes()
    #
    # def getViewMatrix(self):
    #     # THIS HAS A LOT OF HARD CODED STUFF
    #     # we first calculate camera x, y, z axises and from those we assemble a rotation matrix.
    #     # Once that is done we add in the translation.
    #     # We assume camera always look at the world space origin.
    #     # Up vector is always in the direction of global yAxis.
    #     # camZAxis = normalize(
    #     #     numpy.array([-self.camPosition[0], -self.camPosition[1], -self.camPosition[2], 0.0], dtype='float32'))
    #     # camXAxis = cross(camZAxis, self.camUpAxis)
    #     # camYAxis = cross(camXAxis, camZAxis)
    #     # camZAxis = Vector3f(-self.camPosition.x(), -self.camPosition.y(), -self.camPosition.z())
    #
    #     # camZAxis = self.camCenter - self.camPosition
    #     # camZAxis = camZAxis.normalize()
    #     # camXAxis = camZAxis.cross(self.camUpAxis)
    #     #
    #     # camYAxis = camXAxis.cross(camZAxis)
    #     rotMat = Matrix.create([self.camXAxis.x(), self.camXAxis.y(), self.camXAxis.z(), 0.0,
    #                             self.camYAxis.x(), self.camYAxis.y(), self.camYAxis.z(), 0.0,
    #                             -self.camZAxis.x(), -self.camZAxis.y(), -self.camZAxis.z(), 0.0,
    #                             0.0, 0.0, 0.0, 1.0])
    #     traMat = Matrix.create([1.0, 0.0, 0.0, -self.camPosition.x(),
    #                             0.0, 1.0, 0.0, -self.camPosition.y(),
    #                             0.0, 0.0, 1.0, -self.camPosition.z(),
    #                             0.0, 0.0, 0.0, 1.0])
    #     return traMat.product(rotMat).asNumpy()
    #

