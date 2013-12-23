#!/usr/bin/env python

import argparse
import sys

from OpenGL.GL import (
        glGetString,
        GL_RENDERER,
        GL_VERSION,
        GL_VENDOR,
        GL_EXTENSIONS,
        )

from OpenGL.GLUT import *

import yaml

import core
import app

config = app.Config(yaml.load("""
    app:
        window:
            height: 600
            width: 800
        bindings:
            key_escape: exit
            key_w: move_forward
            key_s: move_backward
            key_a: move_left
            key_d: move_right
            key_W: pitch_forward
            key_S: pitch_backward
            key_A: yaw_left
            key_D: yaw_right
    """))

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False)

    args = parser.parse_args()

    if args.verbose:
        core.set_log_level('debug')

    # Initialize the window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("--VOXEL--")
    glutIgnoreKeyRepeat(1)

    # Create application and bind functions to GLUT
    a = app.App(config)

    glutDisplayFunc(a.display)
    glutIdleFunc(a.idle)
    glutReshapeFunc(a.resize)
    glutKeyboardFunc(a.keyboard)
    glutKeyboardUpFunc(a.keyboard_up)
    glutMouseFunc(a.mouse_press)
    glutMotionFunc(a.mouse_move)

    # Log diagnostic information
    core.log.debug("GL_RENDERER   = %s" % (glGetString(GL_RENDERER),))
    core.log.debug("GL_VERSION    = %s" % (glGetString(GL_VERSION),))
    core.log.debug("GL_VENDOR     = %s" % (glGetString(GL_VENDOR),))
    core.log.debug("GL_EXTENSIONS = ")
    for ext in sorted(glGetString(GL_EXTENSIONS).split()):
        core.log.debug("  %s" % (ext,))

    glutMainLoop()

if __name__ == "__main__":
    main()
