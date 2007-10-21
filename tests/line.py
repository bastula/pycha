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

import unittest

import cairo

import pycha.line

class PointTests(unittest.TestCase):
    
    def test_point(self):
        point = pycha.line.Point(2, 3, 1.0, 2.0, "test")
        self.assertEqual(point.x, 2)
        self.assertEqual(point.y, 3)
        self.assertEqual(point.xval, 1.0)
        self.assertEqual(point.yval, 2.0)
        self.assertEqual(point.name, "test")

class LineTests(unittest.TestCase):

    def test_init(self):
        ch = pycha.line.LineChart(None)
        self.assertEqual(ch.points, [])

    def test_updateChart(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
        dataset = (
            ('dataset1', ([0, 1], [1, 1], [2, 3])),
            ('dataset2', ([0, 2], [1, 0], [3, 4])),
            )
        ch = pycha.line.LineChart(surface)
        ch.addDataset(dataset)
        ch._updateXY()
        ch._updateChart()
        self.assertEqual(len(ch.points), 6)
        self.assertEqual(ch.points[0].xval, 0)
        self.assertEqual(ch.points[0].yval, 1)
        self.assertEqual(ch.points[0].x, 0)
        self.assertEqual(ch.points[0].y, 1 - 0.25)
        self.assertEqual(ch.points[0].name, 'dataset1')

        self.assertEqual(ch.points[1].xval, 1)
        self.assertEqual(ch.points[1].yval, 1)
        self.assertEqual(ch.points[1].x, 1/3.0)
        self.assertEqual(ch.points[1].y, 0.75)
        self.assertEqual(ch.points[1].name, 'dataset1')

        self.assertEqual(ch.points[2].xval, 2)
        self.assertEqual(ch.points[2].yval, 3)
        self.assertEqual(ch.points[2].x, 2/3.0)
        self.assertEqual(ch.points[2].y, 0.25)
        self.assertEqual(ch.points[2].name, 'dataset1')

        self.assertEqual(ch.points[3].xval, 0)
        self.assertEqual(ch.points[3].yval, 2)
        self.assertEqual(ch.points[3].x, 0)
        self.assertEqual(ch.points[3].y, 0.5)
        self.assertEqual(ch.points[3].name, 'dataset2')
        
        self.assertEqual(ch.points[4].xval, 1)
        self.assertEqual(ch.points[4].yval, 0)
        self.assertEqual(ch.points[4].x, 1/3.0)
        self.assertEqual(ch.points[4].y, 1)
        self.assertEqual(ch.points[4].name, 'dataset2')

        self.assertEqual(ch.points[5].xval, 3)
        self.assertEqual(ch.points[5].yval, 4)
        self.assertEqual(ch.points[5].x, 1)
        self.assertEqual(ch.points[5].y, 0)
        self.assertEqual(ch.points[5].name, 'dataset2')

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PointTests),
        unittest.makeSuite(LineTests),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

