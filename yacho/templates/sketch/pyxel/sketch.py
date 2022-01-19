# -*- coding: utf-8 -*-
import pyxel


class App:
    def __init__(self):
        pyxel.init(128, 128, title='app')

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(pyxel.COLOR_WHITE)
        pyxel.circ(pyxel.width / 2, pyxel.height / 2, 16, pyxel.COLOR_RED)


if __name__ == '__main__':
    app = App()
    app.run()
