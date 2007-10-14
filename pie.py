import math

import cairo

from pycha.chart import Chart
from pycha.color import Color, hex2rgb

class PieChart(Chart):

    def __init__(self, surface=None, options={}):
        super(PieChart, self).__init__(surface, options)
        self.slices = []

    def render(self, surface=None, options={}):
        """Renders the chart with the specified options.
        
        The optional parameters can be used to render a piechart in a different
        surface with new options.
        """
        self._evaluate(options)
        self._render(surface)
        self._renderPieChart()
        self._renderPieAxis()

    def _evaluate(self, options):
        """Evaluates all the data needed to plot the pie chart"""
        self._eval(options)

        self.centerx = self.area.x + self.area.w * 0.5
        self.centery = self.area.y + self.area.h * 0.5
        self.radius = min(self.area.w * self.options.pieRadius,
                          self.area.h * self.options.pieRadius)

        self._evalPieChart()
        self._evalPieTicks()

    def _evalPieChart(self):
        """Evaluates measures for pie charts"""
        slices = [dict(name=key,
                       value=(i, value[0][1]))
                  for i, (key, value) in enumerate(self.dataSets)]

        s = sum([slice['value'][1] for slice in slices])

        fraction = angle = 0.0

        self.slices = []
        for slice in slices:
            angle += fraction
            if slice['value'][1] > 0:
                fraction = slice['value'][1] / s
                self.slices.append(Slice(slice['name'], fraction,
                                         slice['value'][0], slice['value'][1],
                                         angle))

    def _renderPieChart(self):
        """Renders a pie chart"""
        cx = cairo.Context(self.surface)
        cx.set_line_join(cairo.LINE_JOIN_ROUND)

        if self.options.stroke.shadow:
            cx.save()
            cx.set_source_rgba(0, 0, 0, 0.15)

            cx.new_path()
            cx.move_to(self.centerx, self.centery)
            cx.arc(self.centerx + 1, self.centery + 2, self.radius + 1, 0,
                   math.pi * 2)
            cx.line_to(self.centerx, self.centery)
            cx.close_path()
            cx.fill()
            cx.restore()

        cx.save()
        for slice in self.slices:
            if slice.isBigEnough():
                color = self.options.colorScheme[slice.name]
                cx.set_source_rgb(*hex2rgb(color))
                if self.options.shouldFill:
                    slice.draw(cx, self.centerx, self.centery, self.radius)
                    cx.fill()

                if not self.options.stroke.hide:
                    slice.draw(cx, self.centerx, self.centery, self.radius)
                    cx.set_line_width(self.options.stroke.width)
                    cx.set_source_rgb(*hex2rgb(self.options.stroke.color))
                    cx.stroke()

        cx.restore()

    def _evalPieTicks(self):
        """Evaluates ticks for x and y axis"""
        self.xticks = []

        if self.options.axis.x.ticks:
            lookup = dict([(slice.xval, slice) for slice in self.slices])
            for tick in self.options.axis.x.ticks:
                slice = lookup[tick.v]
                label = tick.label or str(tick.v)
                if not slice:
                    label += ' (%.1f%%)' % (slice.fraction * 100)
                    self.xticks.append((tick.v, label))
        else:
            for slice in self.slices:
                label = '%s (%.1f%%)' % (slice.xval, slice.fraction * 100)
                self.xticks.append((slice.xval, label))

    def _renderPieAxis(self):
        """Renders the axis for pie charts"""
        if self.options.axis.x.hide or not self.xticks:
            return

        self.xlabels = []
        lookup = dict([(slice.xval, slice) for slice in self.slices])

        labelStyle = dict(
            fontFamily=self.options.axis.labelFont,
            fontSize='%dpx' % self.options.axis.labelFontSize,
            )
        cx = cairo.Context(self.surface)
        cx.set_source_rgb(*hex2rgb(self.options.axis.labelColor))

        for tick in self.xticks:
            slice = lookup[tick[0]]

            normalisedAngle = slice.getNormalisedAngle()

            labelx = self.centerx + math.sin(normalisedAngle) * (self.radius + 10)
            labely = self.centery - math.cos(normalisedAngle) * (self.radius + 10)

            label = tick[1]
            extents = cx.text_extents(label)
            labelWidth = extents[2]
            labelHeight = extents[3]
            x = y = 0

            if normalisedAngle <= math.pi * 0.5:
                x = labelx
                y = labely - labelHeight
            elif math.pi * 0.5 < normalisedAngle <= math.pi:
                x = labelx
                y = labely
            elif math.pi < normalisedAngle <= math.pi * 1.5:
                x = labelx - labelWidth
                y = labely
            else:
                x = labelx - labelWidth
                y = labely - labelHeight

            # draw label with text tick[1]
            cx.move_to(x, y)
            cx.show_text(label)
            self.xlabels.append(label)

    def _evalLineTicks(self):
        return

class Slice(object):
    def __init__(self, name, fraction, xval, yval, angle):
        self.name = name
        self.fraction = fraction
        self.xval = xval
        self.yval = yval
        self.startAngle = 2 * angle * math.pi
        self.endAngle = 2 * (angle + fraction) * math.pi

    def isBigEnough(self):
        return abs(self.startAngle - self.endAngle) > 0.001

    def draw(self, cx, centerx, centery, radius):
        cx.new_path()
        cx.move_to(centerx, centery)
        cx.arc(centerx, centery, radius,
               self.startAngle - math.pi/2,
               self.endAngle - math.pi/2)
        cx.line_to(centerx, centery)
        cx.close_path()
    
    def getNormalisedAngle(self):
        normalisedAngle = (self.startAngle + self.endAngle) / 2

        if normalisedAngle > math.pi * 2:
            normalisedAngle -= math.pi * 2
        elif normalisedAngle < 0:
            normalisedAngle += math.pi * 2

        return normalisedAngle