import cairo

from pycha.chart import DEFAULT_OPTIONS
from pycha.bar import VerticalBarChart

from chavier.gui import GUI

class App(object):
    def __init__(self):
        self.gui = GUI(self)

    def run(self):
        self.gui.run()

    def get_default_options(self):
        return DEFAULT_OPTIONS

    def get_chart(self, datasets, options, width, height):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        chart = VerticalBarChart(surface, DEFAULT_OPTIONS)
        chart.addDataset(datasets)
        chart.render()
        return surface

if __name__ == '__main__':
    app = App()
    app.run()
