# Copyright (c) 2007 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#
# This file is part of PyCha.
#
# PyCha is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyCha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PyCha.  If not, see <http://www.gnu.org/licenses/>.

import cairo

import pycha.pie
import pycha.bar
import pycha.line

def testPie():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 400)

    chart = pycha.pie.PieChart(surface)
    dataSet = (
        ('myFirstDataset', [[0, 3]]),
        ('mySecondDataset', [[0, 1.4]]),
        ('myThirdDataset', [[0, 0.46]]),
        ('myFourthDataset', [[0, 0.3]]),
        )

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png("testpie.png")

def testBar():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 300)

    options = {
        'legend': {
            'position': {
                'left': 330
                }
            },
        }

    chart = pycha.bar.VerticalBarChart(surface, options)

    dataSet = (
        ('myFirstDataset', [[0, 1], [1, 1], [2, 1.414], [3, 1.73]]),
	('mySecondDataset', [[0, 0.3], [1, 2.67], [2, 1.34], [3, 1.73]]),
	('myThirdDataset', [[0, 0.46], [1, 1.45], [2, 2.5], [3, 1.2]]),
	('myFourthDataset', [[0, 0.86], [1, 0.83], [2, 3], [3, 1.73]]),
        )

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png("testbar.png")

def testLine():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 600, 500)

    chart = pycha.line.LineChart(surface)

    dataSet = (
        ('myFirstDataset', [[0, 3], [1, 2], [2, 1.414], [3, 2.3]]),
	('mySecondDataset', [[0, 1.4], [1, 2.67], [2, 1.34], [3, 1.2]]),
	('myThirdDataset', [[0, 0.46], [1, 1.45], [2, 1.0], [3, 1.6]]),
	('myFourthDataset', [[0, 0.3], [1, 0.83], [2, 0.7], [3, 0.2]]),
        )

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png("testline.png")


testPie()
testBar()
testLine()
