# Copyright (c) 2007-2008 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#
# This file is part of Chavier.
#
# Chavier is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chavier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Chavier.  If not, see <http://www.gnu.org/licenses/>.

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

    OPTIONS_TYPES = dict(
        axis=dict(
            lineWidth=float,
            lineColor=str,
            tickSize=float,
            labelColor=str,
            labelFont=str,
            labelFontSize=int,
            labelWidth=float,
            x=dict(
                hide=bool,
                ticks=list,
                tickCount=int,
                tickPrecision=int,
                range=list,
                rotate=float,
                label=unicode,
                ),
            y=dict(
                hide=bool,
                ticks=list,
                tickCount=int,
                tickPrecision=int,
                range=list,
                rotate=float,
                label=unicode,
                ),
            ),
        background=dict(
            hide=bool,
            baseColor=str,
            chartColor=str,
            lineColor=str,
            lineWidth=float,
            ),
        legend=dict(
            opacity=float,
            borderColor=str,
            hide=bool,
            position=dict(
                top=int,
                left=int,
                bottom=int,
                right=int,
                )
            ),
        padding=dict(
            left=int,
            right=int,
            top=int,
            bottom=int,
            ),
        stroke=dict(
            color=str,
            hide=bool,
            shadow=bool,
            width=int,
            ),
        fillOpacity=float,
        shouldFill=bool,
        barWidthFillFraction=float,
        pieRadius=float,
        colorScheme=str,
        title=unicode,
        titleFont=str,
        titleFontSize=int,
        )

    def __init__(self):
        self.gui = GUI(self)

    def run(self):
        self.gui.run()

    def get_default_options(self):
        return DEFAULT_OPTIONS

    def get_chart(self, datasets, options, chart_type, width, height):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        chart_factory = self.CHART_TYPES[chart_type]
        chart = chart_factory(surface, options)
        chart.addDataset(datasets)
        chart.render()
        return chart

if __name__ == '__main__':
    app = App()
    app.run()
