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

import pycha.chart

class FunctionsTests(unittest.TestCase):
    
    def test_uniqueIndices(self):
        arr = (range(10), range(5), range(20), range(30))
        self.assertEqual(pycha.chart.uniqueIndices(arr), range(30))

        arr = (range(30), range(20), range(5), range(10))
        self.assertEqual(pycha.chart.uniqueIndices(arr), range(30))

        arr = (range(4),)
        self.assertEqual(pycha.chart.uniqueIndices(arr), range(4))

        arr = (range(0),)
        self.assertEqual(pycha.chart.uniqueIndices(arr), [])

class AreaTests(unittest.TestCase):
    
    def test_area(self):
        area = pycha.chart.Area(10, 20, 100, 300)
        self.assertEqual(area.x, 10)
        self.assertEqual(area.y, 20)
        self.assertEqual(area.w, 100)
        self.assertEqual(area.h, 300)

class OptionTests(unittest.TestCase):
    
    def test_options(self):
        opt = pycha.chart.Option(a=1, b=2, c=3)
        self.assertEqual(opt.a, opt['a'])
        self.assertEqual(opt.b, 2)
        self.assertEqual(opt['c'], 3)

        opt = pycha.chart.Option({'a':1, 'b':2, 'c':3})
        self.assertEqual(opt.a, opt['a'])
        self.assertEqual(opt.b, 2)
        self.assertEqual(opt['c'], 3)

    def test_merge(self):
        opt = pycha.chart.Option(a=1, b=2,
                                 c=pycha.chart.Option(d=4, e=5))
        self.assertEqual(opt.c.d, 4)
        opt.merge(dict(c=pycha.chart.Option(d=7, e=8, f=9)))
        self.assertEqual(opt.c.d, 7)
        # new attributes not present in original option are not merged
        self.assertRaises(AttributeError, getattr, opt.c, 'f')
        
        opt.merge(pycha.chart.Option(a=10, b=20))
        self.assertEqual(opt.a, 10)
        self.assertEqual(opt.b, 20)

class ChartTests(unittest.TestCase):
    
    def test_init(self):
        ch = pycha.chart.Chart(None)
        self.assertEqual(ch.resetFlag, False)
        self.assertEqual(ch.datasets, [])
        self.assertEqual(ch.area, None)
        self.assertEqual(ch.minxval, None)
        self.assertEqual(ch.maxxval, None)
        self.assertEqual(ch.minyval, None)
        self.assertEqual(ch.maxyval, None)
        self.assertEqual(ch.xscale, 1.0)
        self.assertEqual(ch.yscale, 1.0)
        self.assertEqual(ch.xticks, [])
        self.assertEqual(ch.yticks, [])
        self.assertEqual(ch.options, pycha.chart.DEFAULT_OPTIONS)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FunctionsTests),
        unittest.makeSuite(AreaTests),
        unittest.makeSuite(OptionTests),
        unittest.makeSuite(ChartTests),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

