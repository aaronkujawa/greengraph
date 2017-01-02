from nose.tools import assert_raises, assert_almost_equal
import greengraph_module
from greengraph_module import Greengraph
import geopy
from unittest.mock import patch
import yaml
import os
import numpy as np
from itertools import chain
import requests
from matplotlib import image as img

script_dir = os.path.dirname(__file__)
fixtures = yaml.load(open(os.path.join(script_dir, 'fixtures/greengraph_fixtures.yaml')))

geolocate_fixtures = fixtures['geolocate']

# define a function that can be used as a mock for the geocode function to avoid
# the tests from accessing the internet
def mocked_geocode(place, excactly_one = False):
    code = [[[],[]]]
    code[0][1] = [ geolocate_fixtures[place]['latitude'], geolocate_fixtures[place]['longitude'] ]
    return code

# test the geolocate function

# call the geolocate function with different fixtures and check if it returns the
# expected outputs
def test_geolocate_no_fail():
    for place_frm in geolocate_fixtures:
        for place_to in geolocate_fixtures:
            with patch.object(geopy.geocoders.GoogleV3, 'geocode', return_value = mocked_geocode(place_frm)) as mock_geocode:
                graph = Greengraph(place_frm, place_to)
                lat, lng = graph.geolocate(place_frm)
                mock_geocode.assert_called_with(place_frm, exactly_one=False)
                assert_almost_equal(geolocate_fixtures[place_frm]['latitude'], lat)
                assert_almost_equal(geolocate_fixtures[place_frm]['longitude'], lng)


# test the location_sequence function

location_sequence_fixtures = fixtures['location_sequence']

def test_location_sequence_no_fail():
    graph = Greengraph('London', 'Berlin')
    for steps in location_sequence_fixtures:
        with patch.object(geopy.geocoders.GoogleV3, 'geocode', side_effect = [
        mocked_geocode('London'), mocked_geocode('Berlin')] ) as mock_geocode:
            out = graph.location_sequence(graph.geolocate('London'),
            graph.geolocate('Berlin'), steps)
            np.testing.assert_almost_equal(out, location_sequence_fixtures[steps])

def test_location_sequence_fails_on_non_integer_steps():
    with assert_raises(TypeError) as exception:
        graph = Greengraph('New York', 'Chicago')
        graph.location_sequence('New York', 'Chicago', 10.1)

def test_location_sequence_fails_on_value_smaller_than_two():
    with assert_raises(ValueError) as exception:
        graph = Greengraph('New York', 'Chicago')
        graph.location_sequence('New York', 'Chicago', 1)

# test the green_between function
green_between_fixtures = fixtures['green_between']

def test_green_between_no_fail():
    graph = Greengraph('London', 'Berlin')
    for steps in green_between_fixtures:
        with patch.object(geopy.geocoders.GoogleV3, 'geocode', side_effect = [
        mocked_geocode('London'), mocked_geocode('Berlin')] ) as mock_geocode:
            with patch.object(greengraph_module, 'Map') as mock_map:
                with patch.object(mock_map.return_value, 'count_green',
                side_effect = green_between_fixtures[steps] ) as mock_count_green:
                    out = graph.green_between(steps)
                    out = list(chain.from_iterable(np.vstack(out).tolist()))
                    np.testing.assert_almost_equal(out, green_between_fixtures[steps])

def test_green_between_fails_on_non_integer_steps():
    with assert_raises(TypeError) as exception:
        graph = Greengraph('New York', 'Chicago')
        graph.green_between(10.1)

def test_green_between_fails_on_value_smaller_than_two():
    with assert_raises(ValueError) as exception:
        graph = Greengraph('New York', 'Chicago')
        graph.green_between(1)
