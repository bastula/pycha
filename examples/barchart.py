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

import sys

import cairo

import pycha.bar

from lines import lines

def barChart(output):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 200)

    dataSet = (
        ('lines', [(i, l[1]) for i, l in enumerate(lines)]),
        )

    options = {
        'axis': {
            'x': {
                'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(lines)],
            },
            'y': {
                'tickCount': 4,
            }
        },
        'background': {
            'color': '#eeeeff',
            'lineColor': '#444444'
        },
        'colorScheme': 'red',
        'legend': {
            'hide': True,
        },
        'padding': {
            'left': 40
        }
    }
    chart = pycha.bar.VerticalBarChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

if __name__ == '__main__':
    output = sys.argv[1] if len(sys.argv) > 1 else 'barchart.png'
    barChart(output)