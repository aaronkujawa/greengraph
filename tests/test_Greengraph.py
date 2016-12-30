# import socket
# def guard(*args, **kwargs):
#     raise Exception("Tests are not supposed to access the internet.")
# socket.socket = guard

from nose.tools import assert_raises, assert_almost_equal
import greengraph_module
import geopy
from greengraph_module import Greengraph
from unittest.mock import patch
import yaml
import os


script_dir = os.path.dirname(__file__)
fixtures = yaml.load(open(os.path.join(script_dir, 'fixtures/greengraph_fixtures.yaml')))

print(fixtures)

def test_geolocate_no_fail():
    with patch.object(geopy.geocoders.GoogleV3, 'geocode') as mock_geocode:
        graph = Greengraph('New York', 'Chicago')
        graph.geolocate('New York')

def test_location_sequence_no_fail():
        graph = Greengraph('New York', 'Chicago')
        graph.location_sequence([51.5073509, -0.1277583], [0, 0], 10)

def test_location_sequence_fails_on_non_integer_steps():
    with assert_raises(TypeError) as exception:
        graph = Greengraph('New York', 'Chicago')
        graph.location_sequence('New York', 'Chicago', 10.1)


def test_location_sequence_fails_on_value_smaller_than_two():
    with assert_raises(ValueError) as exception:
        graph = Greengraph('New York', 'Chicago')
        graph.location_sequence('New York', 'Chicago', 1)


# def test_energy_fails_on_negative_density():
#    with assert_raises(ValueError) as exception:
#        energy([-1, 2, 3])
