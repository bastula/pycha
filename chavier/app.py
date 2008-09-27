import cairo

from pycha.chart import DEFAULT_OPTIONS
import pycha.bar
import pycha.line
import pycha.pie
import pycha.scatter

from chavier.gui import GUI

class App(object):

    CHART_TYPES = (
        pycha.bar.VerticalBarChart,
        pycha.bar.HorizontalBarChart,
        pycha.line.LineChart,
        pycha.pie.PieChart,
        pycha.scatter.ScatterplotChart,
        )

    (VERTICAL_BAR_TYPE,
     HORIZONTAL_BAR_TYPE,
     LINE_TYPE,
     PIE_TYPE,
     SCATTER_TYPE) = range(len(CHART_TYPES))

    def __init__(self):
        self.gui = GUI(self)

    def run(self):
        self.gui.run()

    def get_default_options(self):
        return DEFAULT_OPTIONS

    def get_chart(self, datasets, options, chart_type, width, height):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        chart_factory = self.CHART_TYPES[chart_type]
        chart = chart_factory(surface, DEFAULT_OPTIONS)
        chart.addDataset(datasets)
        chart.render()
        return surface

if __name__ == '__main__':
    app = App()
    app.run()
