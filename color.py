class Color(object):

    def __init__(self, color):
        self.toHex(color)

    def toHex(self, color):
        """Parses and stores the hex values of the input color string"""
        # TODO
        self.r = int(color[1:3], 16)
        self.g = int(color[3:5], 16)
        self.b = int(color[5:7], 16)
        return self.check()

    def lighten(self, level):
        """Lightens the color"""
        self.r += level
        self.g += level
        self.b += level
        return self.check()

    def darken(self, level):
        """Darkens the color"""
        self.r -= level
        self.g -= level
        self.b -= level
        return self.check()

    def check(self):
        """Checks and validates if the hex values r, g and b are
        between 0 and 255"""
        self.r = clamp(0, 255, self.r)
        self.g = clamp(0, 255, self.g)
        self.b = clamp(0, 255, self.b)
        return self

    def toHexString(self):
        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    def toRgbString(self):
        return 'rgb(%d, %d, %d)' % (self.r, self.g, self.b)

    def toRgbaString(self, alpha):
        return 'rgb(%d, %d, %d, %d)' % (self.r, self.g, self.b, alpha)

def generateColorscheme(hex, keys):
    color = Color(hex)
    return dict([(key, color.lighten(25).toHexString()) for key in keys])

def defaultColorscheme(keys):
    return generateColorscheme('#3c581a', keys)

def getColorscheme(color, keys):
    return generateColorscheme(colorSchemes.get(color, color), keys)

colorSchemes = dict(
    red='#6d1d1d',
    green='#3c581a',
    blue='#224565',
    grey='#444444',
    black='#000000',
    darkcyan='#305755'
    )

def clamp(minValue, maxValue, value):
    if value < minValue:
        return minValue
    if value > maxValue:
        return maxValue
    return value

def hex2rgb(hexstring):
    color = Color(hexstring)
    return color.r / 255.0, color.g / 255.0, color.b / 255.0