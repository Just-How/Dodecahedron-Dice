""" COSC4370 Homework #3 """

import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

vertices = [
    (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
    (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1),
    (0, 1.618, 0.618), (0, 1.618, -0.618), (0, -1.618, 0.618), (0, -1.618, -0.618),
    (0.618, 0, 1.618), (-0.618, 0, 1.618), (0.618, 0, -1.618), (-0.618, 0, -1.618),
    (1.618, 0.618, 0), (-1.618, 0.618, 0), (1.618, -0.618, 0), (-1.618, -0.618, 0)]

edges = [
    (0, 8), (0, 12), (0, 16), (1, 9), (1, 14), (1, 16),
    (2, 10), (2, 12), (2, 18), (3, 11), (3, 14), (3, 18),
    (4, 8), (4, 13), (4, 17), (5, 9), (5, 15), (5, 17),
    (6, 10), (6, 13), (6, 19), (7, 11), (7, 15), (7, 19),
    (8, 9), (10, 11), (12, 13), (14, 15), (16, 18), (17, 19)]

texture_coords = [
    [(0.165, 0.749), (0.331, 0.860), (0.268, 1), (0.062, 1), (0, 0.860)], # 1
    [(0.496, 0.749), (0.666, 0.860), (0.603, 1), (0.393, 1), (0.331, 0.860)], # 2
    [(0.835, 0.749), (1, 0.860), (0.939, 1), (0.728, 1), (0.666, 0.860)], # 3
    [(0, 0.611), (0.062, 0.749), (0.268, 0.749), (0.331, 0.611), (0.165, 0.500)], # 4
    [(0.496, 0.500), (0.666, 0.611), (0.603, 0.749), (0.393, 0.749), (0.331, 0.611)], # 5
    [(0.835, 0.500), (1, 0.611), (0.939, 0.749), (0.728, 0.749), (0.666, 0.611)], # 6
    [(0, 0.36), (0.062, 0.497), (0.268, 0.497), (0.331, 0.36), (0.165, 0.249)], # 7
    [(0.496, 0.249), (0.666, 0.36), (0.603, 0.497), (0.393, 0.497), (0.331, 0.36)], # 8
    [(0.835, 0.249), (1, 0.36), (0.939, 0.497), (0.728, 0.497), (0.666, 0.36)], # 9
    [(.165,0), (.331,.11), (.269,.249), (0.062, .249), (0, .11)], # 10
    [(0.496, 0), (0.666, 0.109), (0.603, 0.249), (0.393, 0.249), (0.331, 0.109)], # 11
    [(0.835, 0), (1, 0.109), (0.939, 0.249), (0.728, 0.249), (0.666, 0.109)]] # 12 

surfaces = [
    [0, 16, 1, 9, 8], [0, 8, 4, 13, 12], [4, 8, 9, 5, 17],
    [2, 10, 6, 13, 12], [1, 16, 18, 3, 14], [5, 9, 1, 14, 15],
    [0, 16, 18, 2, 12], [3, 14, 15, 7, 11], [6, 10, 11, 7, 19],
    [15, 5, 17, 19, 7], [10, 2, 18, 3, 11], [4, 17, 19, 6, 13]]

forced = False

def Dodecahedron(vx, vy, vz, texture):
    for surface_index, surface in enumerate(surfaces):
        glBegin(GL_POLYGON)
        for vertex_index, vertex in enumerate(surface):
            glTexCoord2fv(texture[surface_index][vertex_index])
            glVertex3fv(vertices[vertex])
        glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def loadTexture():
    textureSurface = pygame.image.load('num2.png')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid

pygame.init()
display = (800, 800)
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("COSC4370 Homework #3")

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

loadTexture()

run = True
angle = 0 #Rotation angle about the vertical axis
glColor(1,1,1,1)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN: #Capture an escape key press to exit
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False

    #init model view matrix
    glLoadIdentity()

    #apply view matrix
    glMultMatrixf(viewMatrix)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glColor(1,1,1,1)
    tilt = 15 + 10 * math.cos(angle * math.pi/180) #Tilt as we rotate
    glRotate(tilt, 1, 0, 0) #Tilt a bit to be easier to see
    angle = (angle + 1) % 360
    glRotatef(angle, 0, 0, 1) #Rotate around the box's vertical axis
    Dodecahedron(0,0,0,texture_coords)

    glColor4f(0.5, 0.5, 0.5, 1)
    glBegin(GL_POLYGON)
    glVertex3f(-10, -10, -2)
    glVertex3f(10, -10, -2)
    glVertex3f(10, 10, -2)
    glVertex3f(-10, 10, -2)
    glEnd()

    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()
