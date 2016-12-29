from nose.tools import assert_raises, assert_almost_equal
import greengraph
import geopy
from greengraph import Greengraph
from unittest.mock import patch

def test_geolocate_no_fail():
    with patch.object(geopy.geocoders.GoogleV3, 'geocode') as mock_geocode:
        graph = Greengraph('New York', 'Chicago')
        print( 'HEEEEEERREREEEE20')
        print (graph.geocoder.geocode.mock_calls)
        graph.geolocate('New York')
        print( 'HEEEEEERREREEEE30')
        print (graph.geocoder.geocode.mock_calls)
        graph.geolocate('New York')
        print (graph.geocoder.geocode.mock_calls)

def test_location_sequence_no_fail():
    with patch.object(geopy.geocoders.GoogleV3, 'geocode') as mock_geocode:
        graph = Greengraph('New York', 'Chicago')
        graph.location_sequence([51.5073509, -0.1277583], [0, 0], 10)

def test_location_sequence_fails_on_non_integer_steps():
    print( 'HEEEEEERREREEEE')
    with assert_raises(TypeError) as exception:
        print( 'HEEEEEERREREEEE2')
        with patch.object(geopy.geocoders.GoogleV3, 'geocode') as mock_geocode:
            print( 'HEEEEEERREREEEE3')
            graph = Greengraph('New York', 'Chicago')
            graph.location_sequence('New York', 'Chicago', 10.1)


def test_location_sequence_fails_on_integer_smaller_than_two():
    with assert_raises(ValueError) as exception:
        graph = Greengraph('New York', 'Chicago')
        graph.location_sequence('New York', 'Chicago', 1)


# def test_energy_fails_on_negative_density():
#    with assert_raises(ValueError) as exception:
#        energy([-1, 2, 3])
