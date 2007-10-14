import cairo

from pycha.color import defaultColorscheme, getColorscheme, hex2rgb

class Chart(object):

    def __init__(self, surface, options={}):
        self.resetFlag = False

        # initialize storage hash
        self.dataSets = []

        # override the default options
        self.setOptions(options)

        # initialize the canvas
        self._initCanvas(surface)

    def addDataset(self, dataset):
        """Adds an object containing chart data to the storage hash"""
        self.dataSets += dataset

    def getDataSetsKeys(self):
        return [d[0] for d in self.dataSets]

    def getDataSetsValues(self):
        return [d[1] for d in self.dataSets]

    def setOptions(self, options={}):
        """Sets options of this chart"""
        self.options = Option(
            axis=Option(
                lineWidth=1.0,
                lineColor='#000000',
                tickSize=3.0,
                labelColor='#666666',
                labelFont='Tahoma',
                labelFontSize=9,
                labelWidth=50.0,
                x=Option(
                    hide=False,
                    ticks=None,
                    tickCount=10,
                    tickPrecision=1,
                    range=None,
                ),
                y=Option(
                    hide=False,
                    ticks=None,
                    tickCount=10,
                    tickPrecision=1,
                    range=None,
                ),
            ),
            background=Option(
                color='#f5f5f5',
                hide=False,
                lineColor='#ffffff',
                lineWidth=1.5,
            ),
            legend=Option(
                opacity=0.8,
                borderColor='#000000',
                style={},
                hide=False,
                position=Option(top='20px', left='40px'),
            ),
            padding=Option(
                left=30,
                right=30,
                top=5,
                bottom=10,
            ),
            stroke=Option(
                color='#ffffff',
                hide=False,
                shadow=True,
                width=2
            ),
            fillOpacity=1.0,
            shouldFill=True,
            barWidthFillFraction=0.75,
            barOrientation='vertical',
            xOriginIsZero=True,
            yOriginIsZero=True,
            pieRadius=0.4,
            colorScheme=defaultColorscheme(self.getDataSetsKeys()),
        )#.update(options)
        

    def reset(self):
        """Resets options and datasets"""
        self.resetFlag = True
        self.setOptions()
        self.dataSets = []

    def _initCanvas(self, surface):
        if self.resetFlag:
            self.resetFlag = False
            self.clean()
        
        self.surface = surface
        
    def _render(self, surface=None):
        """Function that does basic rendering of the legend and background.
        
        This function is called by all charts
        """
        if surface:
            self._initCanvas(surface)
        
        self._renderBackground()
        self._renderLegend()

    def clean(self):
        """Clears a canvas tag.
        
        This removes all renderings including axis, legends etc
        """
        # TODO clearRect the canvas
    
    def _renderLegend(self):
        """This function adds a legend to the chart"""
        if self.options.legend.hide:
            return
        # TODO
        
    def setColorscheme(self):
        """Sets the colorScheme used for the chart"""
        scheme = self.options.colorScheme
        if isinstance(scheme, object):
            return
        elif isinstance(scheme, basestring):
            self.options.colorScheme = getColorscheme(scheme,
                                                      self.getDataSetsKeys())
        else:
            raise TypeError("Color scheme is invalid!")

    def _renderBackground(self):
        """Renders the background of the chart"""
        if self.options.background.hide:
            return
        
        cx = cairo.Context(self.surface)
        cx.save()
        cx.set_source_rgb(*hex2rgb(self.options.background.color))
        cx.paint()
        cx.set_source_rgb(*hex2rgb(self.options.background.lineColor))
        cx.set_line_width(self.options.axis.lineWidth)
        
        return

        if self.type == 'pie':
            cx.restore()
            return
        
        ticks = self.yticks
        horiz = False
        if self.type == 'bar' and self.options.barOrientation == 'horizontal':
            ticks = self.xticks
            horiz = True
        
        def drawLine(tick):
            x1, x2, y1, y2 = (0, 0, 0, 0)
            if horiz:
                x1 = x2 = tick[0] * self.area.w + self.area.x
                y1 = self.area.y
                y2 = y1 + self.area.h
            else:
                x1 = self.area.x
                x2 = x1 + self.area.w
                y1 = y2 = tick[0] * self.area.h + self.area.y

            cx.begin_path()
            cx.move_to(x1, y1)
            cx.line_to(x2, y2)
            cx.close_path()
            cx.stroke()

        for tick in ticks:
            drawLine(tick)
        
        cx.restore()

    def _renderLineAxis(self):
        """Renders the axis for line charts"""
        self._renderAxis()
    
    def _renderAxis(self):
        """Renders axis"""
        if self.options.axis.x.hide and self.options.axis.y.hide:
            return
        
        cx = cairo.Context(self.surface)
        cx.save()
        cx.set_source_rgb(*hex2rgb(self.options.axis.lineColor))
        cx.set_line_width(self.options.axis.lineWidth)
        
        if not self.options.axis.y.hide:
            if self.yticks:
                def collectYLabels(tick):
                    if callable(tick):
                        return
                    
                    x = self.area.x
                    y = self.area.y + tick[0] * self.area.h
                    
                    cx.new_path()
                    cx.move_to(x, y)
                    cx.line_to(x - self.options.axis.tickSize, y)
                    cx.close_path()
                    cx.stroke()
                    
                    # TODO, draw the label
                    label = tick[1]
                    return label
                self.ylabels = [collectYLabels(tick) for tick in self.yticks]
                
            cx.new_path()
            cx.move_to(self.area.x, self.area.y)
            cx.line_to(self.area.x, self.area.y + self.area.h)
            cx.close_path()
            cx.stroke()

        if not self.options.axis.x.hide:
            if self.xticks:
                def collectXLabels(tick):
                    if callable(tick):
                        return
                    
                    x = self.area.x + tick[0] * self.area.w
                    y = self.area.y + self.area.h
                    
                    cx.new_path()
                    cx.move_to(x, y)
                    cx.line_to(x, y + self.options.axis.tickSize)
                    cx.close_path()
                    cx.stroke()
                    
                    # TODO, draw the label
                    label = tick[1]
                    return label
                self.xlabels = [collectXLabels(tick) for tick in self.xticks]
            
            cx.new_path()
            cx.move_to(self.area.x, self.area.y + self.area.h)
            cx.line_to(self.area.x + self.area.w, self.area.y + self.area.h)
            cx.close_path()
            cx.stroke()

        cx.restore()

    def _eval(self, options={}):
        """Everytime a chart is rendered, we need to evaluate metric for
        the axis"""
        self.setOptions(options)
        self.stores = self.getDataSetsValues()
        self._evalXY()
        self.setColorscheme()

    def _evalXY(self):
        """Calculates all kinds of metrics for the x and y axis"""
        
        # calculate area data
        width = (self.surface.get_width()
                 - self.options.padding.left - self.options.padding.right)
        height = (self.surface.get_height()
                  - self.options.padding.top - self.options.padding.bottom)
        self.area = Area(self.options.padding.left,
                         self.options.padding.top,
                         width, height)

        # gather data for the x axis
        if self.options.axis.x.range:
            self.minxval, self.maxxval = self.options.axis.x.range
            self.xscale = self.maxxval - self.minxval
        else:
            xdata = [pair[0] for pair in reduce(lambda a,b: a+b, self.stores)]
            self.minxval = 0.0 if self.options.xOriginIsZero else float(min(xdata))
            self.maxxval = float(max(xdata))

        self.xrange = self.maxxval - self.minxval
        self.xscale = 1.0 if self.xrange == 0 else 1 / self.xrange

        # gather data for the y axis
        if self.options.axis.y.range:
            self.minyval, self.maxyval = self.options.axis.y.range
            self.yscale = self.maxyval - self.minyval
        else:
            ydata = [pair[1] for pair in reduce(lambda a,b: a+b, self.stores)]
            self.minyval = 0.0 if self.options.yOriginIsZero else float(min(ydata))
            self.maxyval = float(max(ydata))

        self.yrange = self.maxyval - self.minyval
        self.yscale = 1.0 if self.yrange == 0 else 1 / self.yrange

    def _evalLineTicks(self):
        """Evaluates line ticks for x and y axis"""
        
        # evaluate xTicks
        self.xticks = []
        if self.options.axis.x.ticks:
            for tick in self.options.axis.x.ticks:
                label = str(tick.v) if tick.label is None else tick.label
                pos = self.xscale * (tick.v - self.minxval)
                if 0.0 <= pos <= 1.0:
                    self.xticks.append((pos, label))

        elif self.options.axis.x.tickCount > 0:
            uniqx = uniqueIndices(self.stores)
            roughSeparation = self.xrange / self.options.axis.x.tickCount

            i = j = 0
            while i + 1 < len(uniqx) and j < self.options.axis.x.tickCount:
                if (uniqx[i + 1] - self.minxval) >= (j * roughSeparation):
                    pos = self.xscale * (uniqx[i] - self.minxval)
                    if 0.0 <= pos <= 1.0:
                        self.xticks.append((pos, uniqx[i + 1]))
                        j += 1
                i += 1

        # evaluate yTicks
        self.yticks = []
        if self.options.axis.y.ticks:
            for tick in self.options.y.ticks:
                label = str(tick.v) if tick.label is None else tick.label
                pos = self.yscale * (tick.v - self.minyval)
                if 0.0 <= pos <= 1.0:
                    self.yticks.append((pos, label))

        elif self.options.axis.y.tickCount > 0:
            prec = self.options.axis.y.tickPrecision
            num = self.yrange / self.options.axis.y.tickCount
            roughSeparation = 1 if (num < 1 and prec == 0) else round(num, prec)
            
            for i in range(self.options.axis.y.tickCount + 1):
                yval = self.minyval + (i * roughSeparation)
                pos = 1.0 - ((yval - self.minyval) * self.yscale)
                if 0.0 <= pos <= 1.0:
                    self.yticks.append((pos, round(yval, prec)))

def uniqueIndices(arr):
    return range(max([len(a) for a in arr]))
            
class Area(object):
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

class Option(dict):
    def __getattr__(self, name):
        if name in self.keys():
            return self[name]
        else:
            raise AttributeError(name)
