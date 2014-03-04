#!/usr/bin/env python
#lesson4.py

# See original source and C based tutorial at http://nehe.gamedev.net
#This code was created by Richard Campbell '99

#(ported to Python/PyOpenGL by John Ferguson 2000)
#John Ferguson at hakuin@voicenet.com

#Code ported for use with pyglet by Jess Hill (Jestermon) 2009
#jestermon.weebly.com
#jestermonster@gmail.com

#because these lessons sometimes need  openGL GLUT, you need to install
#pyonlgl as well as pyglet, in order for this sample them to work
#pyopengl ~ http://pyopengl.sourceforge.net
#pyglet   ~ http://www.pyglet.org

import pyglet
from pyglet.gl import *
from pyglet.window import key
from OpenGL.GLUT import * #<<<==Needed for GLUT calls
from objloader import *
from numpy import sin

##################################World
class World(pyglet.window.Window):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    objfile1 = 'resource/predator.obj' 
    objfile2 = 'resource/A10.obj' 
    # objfile = 'resource/complex2.obj' 
    obj = OBJ(objfile1)
    # obj2 = OBJ(objfile2)
    def __init__(self):
        config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
        try:
            super(World, self).__init__(resizable=True, config=config)
        except:
            super(World, self).__init__(resizable=True)
        self.setup()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setup(self):
        self.width  = 640
        self.height = 480
        self.rtri   = 0.0 # (was global)
        self.rquad  = 0.0 # (was global)
        self.InitGL(self.width, self.height)
        pyglet.clock.schedule_interval(self.update, 1/60.0) # update at 60Hz

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self,dt):
        self.DrawGLScene()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_draw(self):
        self.DrawGLScene()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_resize(self,w,h):
        self.ReSizeGLScene(w,h)


    def MakeTransparent(self):
        glDisable(GL_DEPTH_TEST)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)                             
        glEnable (GL_BLEND)                                                            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # A general OpenGL initialization function.  Sets all of the initial parameters.
    def InitGL(self,Width, Height):      # We call this right after our OpenGL window is created.
        glClearColor(0.0, 0.0, 0.0, 0.0) # This Will Clear The background Color To Black
        # glClearColor(0.0, 0.0, 0.5, 1.0) # This Will Clear The background Color To Black
        glClearDepth(1.0)                # Enables Clearing Of The Depth Buffer
        glDepthFunc(GL_LESS)             # The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)          # Enables Depth Testing
        glShadeModel(GL_SMOOTH)          # Enables Smooth Color Shading
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                 # Reset The Projection Matrix
                                         # Calculate The Aspect Ratio Of The Window
        #(pyglet initializes the screen so we ignore this call)
        #gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # for realisitic light diffusion effect
        specLight0 = [0.5, 0.5, 0.5, 1.0];
        glLightfv(GL_LIGHT0, GL_SPECULAR, specLight0);
        glMaterialfv(GL_FRONT, GL_SHININESS, 10.0);
        glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 100, 0.0))

        dens = 0.3 
        glLightfv(GL_LIGHT0, GL_AMBIENT, (dens,dens,dens, 0.0))
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 0.0))

        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        # # glutFullScreenToggle()

        # self.MakeTransparent()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
    def ReSizeGLScene(self,Width, Height):
        if Height == 0:                           # Prevent A Divide By Zero If The Window Is Too Small
              Height = 1
        glViewport(0, 0, Width, Height)     # Reset The Current Viewport And Perspective Transformation
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def DrawHUD(self,basicT=(0,0,0)):
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # glOrtho ( 0, 640, 480, 0, 0, 1 )

        glMatrixMode(GL_MODELVIEW)
        # glTranslatef(0, 0, -30.0)
        pyglet.gl.glColor4f(0.0,1,0,1.0)                                               
        glEnable (GL_LINE_SMOOTH);                                                     
        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)                                     
        glLineWidth (3)                                                                
        pyglet.graphics.draw ( 2, pyglet.gl.GL_LINES, ('v2i',(10, 15, 300, 305))    )

        # glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(1.0, 1.0, -6.0)

        # Draw a square (quadrilateral) rotated on the X axis.
        glRotatef(self.rquad, 0.0, 1.0, 0.0)        # Rotate
        glColor3f(1.0, 1.0, 1.0)            # Bluish shade
        glPointSize(3.0)



        glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
        glVertex3f(-1.0, 1.0, 0.0)          # Top Left
        glVertex3f(1.0, 1.0, 0.0)           # Top Right
        glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
        glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
        glEnd()                             # We are done with the polygon

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # The main drawing function.
    def DrawGLScene(self):
        global rtri, rquad

        # Clear The Screen And The Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        basicT = (1,1,1)

        self.DrawHUD(basicT)

        glLoadIdentity()                    # Reset The View
        glTranslatef(15.0, -5, -50.0)
        # glTranslatef(15.0, 2*sin(self.rquad/50.)-5, -50.0)
        glRotatef(20*sin(self.rquad/20.), 0.1, 0.1, -1.0)      # Rotate
        glCallList(self.obj.gl_list)

# ---------------------------------------------------------------------------------
        # We are "undoing" the rotation so that we may rotate the quad on its own axis.
        # We also "undo" the prior translate.  
        # This could also have been done using the matrix stack.

        # # # glLoadIdentity()
        # # # glTranslatef(-15.0, 0.0, -50.0)
        # # # glRotatef(self.rquad, 0.1, -1.0, 0.0)      # Rotate
        # # # glCallList(self.obj2.gl_list)

        # glLoadIdentity()
        # # Move Right 1.5 units and into the screen 6.0 units.
        # glTranslatef(1.0, 1.0, -6.0)
# 
        # # Draw a square (quadrilateral) rotated on the X axis.
        # glRotatef(self.rquad, 0.0, 1.0, 0.0)      # Rotate
        # glColor3f(0.3, 0.5, 1.0)            # Bluish shade
        # glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
        # glVertex3f(-1.0, 1.0, 0.0)          # Top Left
        # glVertex3f(1.0, 1.0, 0.0)           # Top Right
        # glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
        # glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
        # glEnd()                             # We are done with the polygon

        # What values to use?  Well, if you have a FAST machine and a FAST 3D Card, then
        # large values make an unpleasant display with flickering and tearing.  I found that
        # smaller values work better, but this was based on my experience.
        #(2009.. 9 years after this code was written, this still applies.. unless you use)
        #(a timed display, as done here with pyglet.clock.schedule_interval(self.update, 1/60.0) #updates at 60Hz)
        # self.rtri  = self.rtri + 1.0                  # Increase The Rotation Variable For The Triangle
        self.rquad = self.rquad + 1.3                 # Decrease The Rotation Variable For The Quad


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')
        #  since this is double buffered, swap the buffers to display what just got drawn.
        #(pyglet provides the swap, so we dont use the swap here)
        #glutSwapBuffers()

default_size = 1024,768 
screen_size1 = 640,480 
if __name__ == "__main__":
    window = World()
    window.set_location(10,30)
    window.set_size(*screen_size1)
    # window.set_fullscreen(True)
    pyglet.app.run()





