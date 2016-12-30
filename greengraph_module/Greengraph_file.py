import geopy
import numpy as np

import greengraph_module
print ('greengraph_module folder')
print (greengraph_module.__file__)

class Greengraph(object):
    def __init__(self, start, end):
        self.start=start
        self.end=end
        self.geocoder=geopy.geocoders.GoogleV3(domain="maps.google.co.uk")

    def geolocate(self, place):
        return self.geocoder.geocode(place, exactly_one=False)[0][1]

    def location_sequence(self, start, end, steps):

        # test if "steps" can be converted to integer
        try:
            steps = int(steps)
        except:
            raise TypeError('The argument "steps" has to be an integer.')

        # test if "steps" is positive
        if steps < 2:
            raise ValueError('The argument "steps" has to be at least 2.')

        lats = np.linspace(start[0], end[0], steps)
        longs = np.linspace(start[1],end[1], steps)
        return np.vstack([lats, longs]).transpose()

    def green_between(self, steps):
        return [greengraph_module.Map(*location).count_green() for location in self.location_sequence(
        self.geolocate(self.start), self.geolocate(self.end), steps)]
