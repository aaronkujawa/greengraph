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
import requests
from matplotlib import image as img
from PIL import Image
import io

# normal run
default_map = Map(51.1, 0.0)

# create mock content of the request.get function
w, h = 5, 5
data = np.zeros((h, w, 3), dtype=np.uint8)
data[:,2,1] = 1
buffer = io.BytesIO()
img.imsave(buffer, data, format="png")

green_expected_result = data[:,:,1].astype(bool)
count_green_expected_result = np.sum(data)

class mocked_get(object):
    def __init__(self, base, params):
        self.content = buffer.getvalue()

threshold = 1.1;

# test green function
def test_green_function_no_fail():
    with patch.object(requests,'get', mocked_get) as mock_get:
        default_map = Map(51.0, 0.0)
        np.testing.assert_almost_equal((default_map.green(threshold)), green_expected_result)

# test count_green function
def test_count_green_no_fail():
    with patch.object(requests,'get', mocked_get) as mock_get:
        default_map = Map(51.0, 0.0)
        np.testing.assert_almost_equal(default_map.count_green(threshold), count_green_expected_result)

default_map = Map(51.0, 0.0)
default_map.show_green()
# test show_green function

def test_show_green_no_fai():
    with patch.object(requests,'get', mocked_get) as mock_get:
        default_map = Map(51.0, 0.0)
        result_show_green = default_map.show_green()
        green_pixels = img.imread(io.BytesIO(result_show_green), format='png')
        np.testing.assert_almost_equal(np.sum(green_pixels[:,:,0:3]), default_map.count_green())
        np.testing.assert_almost_equal(green_pixels[:,:,0], 0)
        np.testing.assert_almost_equal(green_pixels[:,:,2], 0)
