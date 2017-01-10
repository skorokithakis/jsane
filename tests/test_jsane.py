import json
import os
import sys
import pytest
import pep8

sys.path.insert(0, os.path.abspath(__file__ + "/../.."))

from jsane import loads, dumps, JSaneException, from_dict
from jsane.traversable import Traversable


class TestClass:
    @pytest.fixture(autouse=True)
    def create_data(self):
        self.json1 = """
        {
          "r": "yo",
          "key_1": "value_1",
          "key_2": {
            "key_21": [
              [2100, 2101],
              [2110, 2111]
            ],
            "key_22": ["l1", "l2"],
            "key_23": {"key_231":"v"},
            "key_24": {
              "key_241": 502,
              "key_242": [
                [5, 0],
                [7, 0]
              ],
              "key_243": {
                "key_2431": [0, 0],
                "key_2432": 504,
                "key_2433": [
                  [11451, 0],
                  [11452, 0]
                ]
              },
              "key_244": {
                "key_2441": {
                  "key_24411": {
                    "key_244111": "v_24411",
                    "key_244112": [[5549, 0]]
                  },
                  "key_24412": "v_24412"
                },
                "key_2442": ["ll1", "ll2"]
              }
            }
          }
        }
        """
        self.dict1 = {"foo": "bar"}

    def test_wrapper(self):
        assert loads(dumps(self.dict1)).r() == self.dict1
        assert json.dumps(self.dict1) == dumps(self.dict1)
        assert self.dict1["foo"] == from_dict(self.dict1).foo.r()
        assert loads(dumps(self.dict1)), Traversable(self.dict1)

    def test_access(self):
        j = loads(self.json1)
        assert j.key_1() == "value_1"
        assert j["r"]() == "yo"
        assert j.key_2.key_21[1][1]() == 2111
        assert j.key_1.r() == "value_1"
        assert j["r"].r() == "yo"
        assert j.key_2.key_21[1][1].r() == 2111

    def test_exception(self):
        j = loads(self.json1)
        with pytest.raises(JSaneException):
            j.key_2.nonexistent[0]()
        with pytest.raises(JSaneException):
            j.key_2.key_21[7]()
        with pytest.raises(JSaneException):
            j.key_2.nonexistent[0].r()
        with pytest.raises(JSaneException):
            j.key_2.key_21[7].r()
        with pytest.raises(JSaneException):
            j.key_1.key_2.r()
        with pytest.raises(IndexError):
            j.key_2.key_24.key_244.key_2442[0].r()[7]
        with pytest.raises(JSaneException):
            j.key_2.key_24.key_244.key_2442[0][7].r()

    def test_default(self):
        j = loads(self.json1)
        assert j.key_1.key_2(None) is None
        assert j.key_2.nonexistent[0]("default") == "default"
        assert j.key_2.key_21[7]("default") == "default"
        assert j.key_1.key_2.r(None) is None
        assert j.key_2.nonexistent[0].r("default") == "default"
        assert j.key_2.key_21[7].r("default") == "default"
        with pytest.raises(IndexError):
            j.key_2.key_24.key_244.key_2442[0].r("default")[7]

    def test_resolution(self):
        j = loads(self.json1)
        assert j.key_2.key_21[0].r() == [2100, 2101]
        assert j.key_2.key_21[0].r() == [2100, 2101]
        assert j.key_2.key_24.key_244.key_2442[0].r()[0] == "l"

    def test_pep8(self):
        pep8style = pep8.StyleGuide([['statistics', True],
                                     ['show-sources', True],
                                     ['repeat', True],
                                     ['ignore', "E501"],
                                     ['paths', [os.path.dirname(
                                         os.path.abspath(__file__))]]],
                                    parse_argv=False)
        report = pep8style.check_files()
        assert report.total_errors == 0
