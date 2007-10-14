import sys

import cairo

from pycha.chart import Chart, uniqueIndices
from pycha.color import Color, hex2rgb, clamp

class BarChart(Chart):

    def __init__(self, surface=None, options={}):
        super(BarChart, self).__init__(surface, options)
        self.bars = []
    
    def render(self, surface=None, options={}):
        """Renders the chart with the specified options.
        
        The optional parameters can be used to render a barchart in a
        different surface with new options.
        """
        self._evaluate(options)
        self._render(surface)
        self._renderBarChart()
        self._renderAxis()
        self._renderLegend()
    
    def _evaluate(self, options={}):
        """Evaluates all the data needed to plot the bar chart"""
        self._eval(options)
        if self.options.barOrientation == 'horizontal':
            self._evalHorizontalBarChart()
        else:
            self._evalVerticalBarChart()
        self._evalBarTicks()
    
    def _evalVerticalBarChart(self):
        """Evaluates measures for vertical bars"""
        uniqx = uniqueIndices(self.stores)
        xdelta = min([abs(uniqx[j] - uniqx[j-1]) for j in range(1, len(uniqx))])

        barWidth = 0
        barWidthForSet = 0
        barMargin = 0
        if len(uniqx) == 1:
            xdelta = 1.0
            self.xscale = 1.0
            self.minxval = uniqx[0]
            barWidth = 1.0 * self.options.barWidthFillFraction
            barWidthForSet = barWidth / len(self.stores)
            barMargin = (1.0 - self.options.barWidthFillFraction) / 2
        else:
            if self.xrange == 1:
                self.xscale = 0.5
            elif self.xrange == 2:
                self.xscale = 1 / 3.0
            else:
                self.xscale = (1.0 - 1 / self.xrange) / self.xrange

            barWidth = xdelta * self.xscale * self.options.barWidthFillFraction
            barWidthForSet = barWidth / len(self.stores)
            barMargin = (xdelta * self.xscale
                         * (1.0 - self.options.barWidthFillFraction)/2)
        
        self.minxdelta = xdelta
        self.bars = []
        
        for i, (name, store) in enumerate(self.dataSets):
            for item in store:
                xval, yval = item
                x = (((xval - self.minxval) * self.xscale)
                    + (i * barWidthForSet) + barMargin)
                y = 1.0 - (yval - self.minyval) * self.yscale
                w = barWidthForSet
                h = (yval - self.minyval) * self.yscale
                rect = Rect(x, y, w, h, xval, yval, name)
                
                if (0.0 <= rect.x <= 1.0) and (0.0 <= rect.y <= 1.0):
                    self.bars.append(rect)

    def _evalHorizontalBarChart(self):
        """Evaluates measures for horizontal bars"""
        uniqx = uniqueIndices(self.stores)
        xdelta = min([abs(uniqx[j] - uniqx[j-1]) for j in range(1, len(uniqx))])

        barWidth = 0
        barWidthForSet = 0
        barMargin = 0
        if len(uniqx) == 1:
            xdelta = 1.0
            self.xscale = 1.0
            self.minxval = uniqx[0]
            barWidth = 1.0 * self.options.barWidthFillFraction
            barWidthForSet = barWidth / len(self.stores)
            barMargin = (1.0 - self.options.barWidthFillFraction) / 2
        else:
            self.xscale = (1.0 - xdelta / self.xrange) / self.xrange
            barWidth = xdelta * self.xscale * self.options.barWidthFillFraction
            barWidthForSet = barWidth / len(self.stores)
            barMargin = xdelta * self.xscale * (1.0 - self.options.barWidthFillFraction) / 2
        
        self.minxdelta = xdelta
        self.bars = []

        for i, (name, store) in enumerate(self.dataSets):
            for item in store:
                xval, yval = item
                y = ((xval - self.minxval) * self.xscale) + (i * barWidthForSet) + barMargin
                x = 0.0
                h = barWidthForSet
                w = (yval - self.minyval) * self.yscale
                y = clamp(0.0, 1.0, y)
                rect = Rect(x, y, w, h, xval, yval, name)
                
                if (0.0 <= rect.x <= 1.0):
                    self.bars.append(rect)
                    
    def _renderBarChart(self):
        """Renders a horizontal/vertical bar chart"""
        cx = cairo.Context(self.surface)

        def drawBar(bar):
            cx.set_line_width(self.options.stroke.width)
            
            # gather bar proportions
            x = self.area.w * bar.x + self.area.x
            y = self.area.h * bar.y + self.area.y
            w = self.area.w * bar.w
            h = self.area.h * bar.h
            
            if w < 1 or h < 1:
                return # don't draw when the bar is too small
            
            if self.options.stroke.shadow:
                cx.set_source_rgba(0, 0, 0, 0.15)
                if self.options.barOrientation == 'vertical':
                    cx.rectangle(x-2, y-2, w+4, h+2)
                else:
                    cx.rectangle(x, y-2, w+2, h+4)
                cx.fill()
            
            if self.options.shouldFill:
                cx.rectangle(x, y, w, h)
                cx.set_source_rgb(*hex2rgb(self.options.colorScheme[bar.name]))
                cx.fill_preserve()
            
            if not self.options.stroke.hide:
                cx.set_source_rgb(*hex2rgb(self.options.stroke.color))
                cx.stroke()
        
        cx.save()
        for bar in self.bars:
            drawBar(bar)
        cx.restore()
    
    def _evalBarTicks(self):
        """Evaluates bar ticks"""
        self._evalLineTicks()
        self.xticks = [(tick[0] + (self.minxdelta * self.xscale) / 2,
                        tick[1]) for tick in self.xticks]

        if self.options.barOrientation == 'horizontal':
            tmp = self.xticks
            self.xticks = [(1.0 - tick[0], tick[1]) for tick in self.yticks ]
            self.yticks = tmp


class Rect(object):
    def __init__(self, x, y, w, h, xval, yval, name):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.xval, self.yval = xval, yval
        self.name = name
