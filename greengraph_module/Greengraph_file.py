import geopy
import numpy as np

import greengraph_module

class Greengraph(object):
    def __init__(self, start, end):
        self.start=start
        self.end=end
        self.geocoder=geopy.geocoders.GoogleV3(domain="maps.google.co.uk")

    # function to test the validity of the steps parameter
    def steps_test(self, steps):
            # test if "steps" is an integer
            if (isinstance( steps, int )) == 0:
                raise TypeError('The argument "steps" has to be an integer.')

            # test if "steps" is positive
            if steps < 2:
                raise ValueError('The argument "steps" has to be at least 2.')
            return 0

    def geolocate(self, place):
        return self.geocoder.geocode(place, exactly_one=False)[0][1]

    def location_sequence(self, start, end, steps):
        self.steps_test(steps)
        lats = np.linspace(start[0], end[0], steps)
        longs = np.linspace(start[1],end[1], steps)
        return np.vstack([lats, longs]).transpose()

    def green_between(self, steps):
        self.steps_test(steps)
        return [greengraph_module.Map(*location).count_green() for location in self.location_sequence(
        self.geolocate(self.start), self.geolocate(self.end), steps)]
