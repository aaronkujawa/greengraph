from nose.tools import assert_raises, assert_almost_equal
import greengraph_module
from greengraph_module import Greengraph
from greengraph_module import Map
import geopy
from unittest.mock import patch
import yaml
import os
import numpy as np
from itertools import chain

# create fixtures for geolocate

graph = Greengraph('London', 'Berlin')

some_places = ['London', 'Berlin', 'Springfield', 'Mettingen']
some_steps = [2,5]
#some_places = ['London']

fixtures={}
script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, 'greengraph_fixtures.yaml'), 'w') as outfile:
    for place in some_places:
        lat, lng = graph.geolocate(place)
        fixtures[place] = {'latitude': lat, 'longitude': lng}
    yaml.dump( {'geolocate': fixtures}, outfile, default_flow_style=False)


# create fixtures for location_sequence
fixtures={}
with open(os.path.join(script_dir, 'greengraph_fixtures.yaml'), 'a') as outfile:
    for steps in some_steps:
        out = graph.location_sequence(graph.geolocate('London'), graph.geolocate('Berlin'), steps)
        fixtures[steps] = out.tolist()
    yaml.dump( {'location_sequence': fixtures}, outfile, default_flow_style=False)

# create fixtures for green_between
fixtures={}
with open(os.path.join(script_dir, 'greengraph_fixtures.yaml'), 'a') as outfile:
    for steps in some_steps:
        out = graph.green_between(steps)
        fixtures[steps] = list(chain.from_iterable(np.vstack(out).tolist()))
    yaml.dump( {'green_between': fixtures}, outfile, default_flow_style=False)
