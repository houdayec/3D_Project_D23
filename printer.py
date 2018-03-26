import sys
from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Variables
light_position = [ 1.0, 1.0, 1.0, 0.0 ];
listNormales = []
listTriangles = []
listVertices = []
listCoordinates = []
centerModel = []

cameraX = 50
cameraY = 50

# Méthode pour initier les paramèters graphiques de la fenêtre
def init():
    global quadric, listNormales, listTriangles, listVertices, listCoordinates, centerModel

    indexLine = 0
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    minZ = 0
    maxZ = 0
    with open('rocket.stl') as fp:
        for line in fp:
            if "normal" in line:
                coordinates = line.split('normal', 1)[1]
                temp = coordinates.split(' ', 1 )[1]
                coordinatesPart2 = temp.split(' ', 1 )[0]
                temp2 = temp.split(' ', 1 )[1]
                coordinatesPart3 = temp2.split(' ', 1 )
                #print(coordinatesPart2, coordinatesPart3[0], coordinatesPart3[1])
                print(coordinatesPart3[1])
                coordsNormal = [ coordinatesPart2, coordinatesPart3[0], coordinatesPart3[1] ]
                listNormales.append(coordsNormal)
                #print(listNormales)

            if "vertex" in line:
                #print(line)
                indexLine = indexLine + 1
                coordinates = line.split('vertex ', 1 )[1]
                #print(coordinates.split(' ', 1 )[0])
                coordinatesPart2 = coordinates.split(' ', 1 )[1]
                x = float(coordinates.split(' ', 1 )[0])
                y = float(coordinatesPart2.split(' ', 1 )[0])
                z = float(coordinatesPart2.split(' ', 1 )[1])

                # Définition de la hitbox pour déterminer le baricentre de lma figure
                if(x < minX):
                    minX = x
                if(x > maxX):
                    maxX = x
                if(y < minY):
                    minY = y
                if(y > maxY):
                    maxY = y
                if(z < minZ):
                    minZ = z
                if(z > maxZ):
                    maxZ = z

                listCoordinates = [ x, y, z]
                #print(listCoordinates)
                listVertices.append(listCoordinates)
                if indexLine%3 == 0:
                    listTriangles.append(listVertices)
                    listVertices = []
                    listCoordinates = []
                    #print("Triangle ", indexLine, "--------------")
    centerModel = [(minX + maxX)/2, (minY + maxY)/2, (minZ + maxZ)/2]
    print("centerModel", centerModel)
    # Set le background en noir
    glClearColor (0.0, 0.0, 0.0, 0.0)
    #glShadeModel (GL_FLAT)
    #quadric = gluNewQuadric()
    # Pour avoir des figures pleines et non plus fil de fer
    #gluQuadricDrawStyle(quadric, GLU_FILL)

    glEnable(GL_DEPTH_TEST)  # Enable depth testing for z-culling

    glShadeModel(GL_SMOOTH)   # Enable smooth shading

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glDisable( GL_CULL_FACE )



def drawModel():
    # Generate 1 display list
    #GLuint list1 = glGenLists( 1 );
    #glNewList( list1, GL_COMPILE );

    # Enter your vertices here

    glColor3f(0.0, 1.0, 0.0)

    i = 0
    for triangle in listTriangles:
        i = i+1
        #print("TRANGLE", triangle, "\n")
        #print(float(triangle[0][0]), float(triangle[0][1]), float(triangle[0][2]))
        glBegin(GL_TRIANGLES)
        #print(listNormales[i])
        glNormal3f(float(listNormales[i][0]), float(listNormales[i][1]), float(listNormales[i][2]))
        glVertex3f(float(triangle[0][0]), float(triangle[0][1]), float(triangle[0][2]))
        glVertex3f(float(triangle[1][0]), float(triangle[1][1]), float(triangle[1][2]))
        glVertex3f(float(triangle[2][0]), float(triangle[2][1]), float(triangle[2][2]))
        glEnd()
        #for vertex in triangle:
            #print(vertex[2])
            #drawBall(vertex[0], vertex[1], vertex[2])
            #for coordinate in vertex:
                #print(coordinate)
                #drawBall(coordinate[0], coordinate[1], coordinate[2])
    #glEndList();
    # Then later, elsewhere in your code,
    # Call the display list to render it
    #glCallList( list1 );


def drawBall(x,y,z):
    ambient = (0.1, 0.1, 0.1, 1.0)
    diffuse = (0.8, 0.8, 0.8, 1.0)
    Black = (0.0, 0.0, 0.0, 1.0)
    sph1 = glutSolidSphere(x,y,z)

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, Black)
    glMaterialfv(GL_FRONT, GL_EMISSION, ambient)
    glMaterialf(GL_FRONT, GL_SHININESS, 0.0)

    gluQuadricDrawStyle(sph1, GLU_FILL)
    gluQuadricNormals(sph1, GLU_SMOOTH)
    gluQuadricTexture(sph1, GL_TRUE)
    glutSolidSphere(sph1, 1, 100, 80)

def display():
    #glEnable(GL_DITHER)
    # Clear l'écran et donne une couleur
    glClearColor(0,0,0,0)
    #glClearDepth(0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Gère les figures affichées avec les rotations et translations
    glPushMatrix()

    gluLookAt(cameraX, cameraY, 200, 10, 0, 0, 0, 1, 0)


    # Définition des types de surface pour les modèles 3D

    glEnable (GL_COLOR_MATERIAL)
    glColorMaterial (GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glMaterial(GL_FRONT, GL_DIFFUSE, 100.0)

    # Affichage de la figure
    drawModel()

    # Gère les figures affichées avec les rotations et translations
    glPopMatrix()

    glutSwapBuffers()

# Réadaptation du screen à la taille définie
def reshape(width, height):
    #Définition du viewport (fenêtre avec taille adaptée)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Redéfinition du repère ortho selon les paramètres height et width
    if width <= height:
	    gluPerspective(50.0, height/width, 1.0, 1000.0)
    else:
        gluPerspective(50.0, width/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)

# Appelées lorsqu'un événement touche est lancé
def keyboard(key, x, y):
    glutPostRedisplay()

###############################################################
# MAIN

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

glutCreateWindow('3Dprinter')
glutReshapeWindow(1024,1024)

glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

init()

glutMainLoop()
