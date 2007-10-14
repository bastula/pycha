import cairo

from pycha.chart import Chart
from pycha.color import Color, hex2rgb, clamp

class LineChart(Chart):
    
    def __init__(self, surface=None, options={}):
        super(LineChart, self).__init__(surface, options)
        self.points = []

    def render(self, surface=None, options={}):
        """Renders the chart with the specified options.
        
        The optional parameters can be used to render a linechart in a
        different surface with new options.
        """
        self._evaluate(options)
        self._render(surface)
        self._renderLineChart()
        self._renderLineAxis()
    
    def _evaluate(self, options={}):
        """Evaluates all the data needed to plot the line chart"""
        self._eval(options)
        self._evalLineChart()
        self._evalLineTicks()
    
    def _evalLineChart(self):
        """Evaluates measures for line charts"""
        self.points = []

        for i, (name, store) in enumerate(self.dataSets):
            for item in store:
                xval, yval = item
                x = (xval - self.minxval) * self.xscale
                y = 1.0 - (yval - self.minyval) * self.yscale
                point = Point(x, clamp(0.0, 1.0, y), xval, yval, name)
                
                if 0.0 <= point.x <= 1.0:
                    self.points.append(point)
    
    def _renderLineChart(self):
        """Renders a line chart"""
        cx = cairo.Context(self.surface)
        
        def preparePath(storeName):
            cx.new_path()
            cx.move_to(self.area.x, self.area.y + self.area.h)
            for point in self.points:
                if point.name == storeName:
                    cx.line_to(point.x * self.area.w + self.area.x,
                               point.y * self.area.h + self.area.y)
            cx.line_to(self.area.w + self.area.x, self.area.h + self.area.y)
            cx.line_to(self.area.x, self.area.y + self.area.h)

            if self.options.shouldFill:
                cx.close_path()
            else:
                cx.set_source_rgb(*hex2rgb(self.options.colorScheme[storeName]))
                cx.stroke()
        

        cx.save()
        cx.set_line_width(self.options.stroke.width)
        if self.options.shouldFill:
            def drawLine(storeName):
                if self.options.stroke.shadow:
                    # draw shadow
                    cx.save()
                    cx.set_source_rgba(0, 0, 0, 0.15)
                    cx.translate(2, -2)
                    preparePath(storeName)
                    cx.fill()
                    cx.restore()
                
                # fill the line
                cx.set_source_rgb(*hex2rgb(self.options.colorScheme[storeName]))
                preparePath(storeName)
                cx.fill()
                
                if not self.options.stroke.hide:
                    # draw stroke
                    cx.set_source_rgb(*hex2rgb(self.options.stroke.color))
                    preparePath(storeName)
                    cx.stroke()

            # draw the lines
            for key in self.getDataSetsKeys():
                drawLine(key)
        else:
            for key in self.getDataSetsKeys():
                preparePath(key)

        cx.restore()

class Point(object):
    def __init__(self, x, y, xval, yval, name):
        self.x, self.y = x, y
        self.xval, self.yval = xval, yval
        self.name = name