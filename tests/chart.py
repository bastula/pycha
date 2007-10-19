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

        arr = (range(4),)
        self.assertEqual(pycha.chart.uniqueIndices(arr), range(4))

class AreaTests(unittest.TestCase):
    
    def test_area(self):
        area = pycha.chart.Area(10, 20, 100, 300)
        self.assertEqual(area.x, 10)
        self.assertEqual(area.y, 20)
        self.assertEqual(area.w, 100)
        self.assertEqual(area.h, 300)

class OptionTests(unittest.TestCase):
    pass

class ChartTests(unittest.TestCase):
    pass

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FunctionsTests),
        unittest.makeSuite(AreaTests),
        unittest.makeSuite(OptionTests),
        unittest.makeSuite(ChartTests),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

