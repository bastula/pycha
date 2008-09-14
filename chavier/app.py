from pycha.chart import DEFAULT_OPTIONS

from chavier.gui import GUI

class App(object):
    def __init__(self):
        self.gui = GUI(self)

    def run(self):
        self.gui.run()

    def get_default_options(self):
        return DEFAULT_OPTIONS

if __name__ == '__main__':
    app = App()
    app.run()
