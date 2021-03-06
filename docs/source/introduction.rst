============
Introduction
============

Pycha is a very simple Python package for drawing charts using the great
`Cairo <http://www.cairographics.org/>`_ library. Its goals are:

* Lightweight
* Simple to use
* Nice looking with default values
* Customization

It won't try to draw any possible chart on earth but draw the most common ones
nicely. There are some other options you may want to look at like
`pyCairoChart <http://bettercom.de/de/pycairochart>`_.

Pycha is based on `Plotr <http://solutoire.com/plotr/>`_ which is based on
`PlotKit <http://www.liquidx.net/plotkit/>`_. Both libraries are written in
JavaScript and are great for client web programming. I needed the same for the
server side so that's the reason I ported Plotr to Python. Now we can deliver
charts to people with JavaScript disabled or embed them in PDF reports.

Pycha is distributed under the terms of the `GNU Lesser General Public License
<http://www.gnu.org/licenses/lgpl.html>`_.
