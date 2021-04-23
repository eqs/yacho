# -*- coding: utf-8 -*-
import sys
import numpy as np
import pyof as of


class ofApp(of.ofPyBaseApp):
    def setup(self):
        of.ofSetWindowTitle('pyof')

    def update(self):
        pass

    def draw(self):
        of.ofBackground(0, 255);


if __name__ == '__main__':
    app = ofApp()
    app.run(800, 800, of.OF_WINDOW)
