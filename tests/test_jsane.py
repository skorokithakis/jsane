import json
import os
import sys
import pytest
import pep8

sys.path.insert(0, os.path.abspath(__file__ + "/../.."))

from jsane import loads, dumps, JSaneException, from_dict, from_object
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
          },
          "numeric_string": "115",
          "list": [1, 1, 2, 3, 5, 8]
        }
        """
        self.dict1 = {"foo": "bar"}

    def test_wrapper(self):
        assert loads(dumps(self.dict1))() == self.dict1
        assert json.dumps(self.dict1) == dumps(self.dict1)
        assert self.dict1["foo"] == from_dict(self.dict1).foo()
        assert loads(dumps(self.dict1)), Traversable(self.dict1)

    def test_access(self):
        j = loads(self.json1)
        assert j.key_1() == "value_1"
        assert j["r"]() == "yo"
        assert j.key_2.key_21[1][1]() == 2111
        assert j.key_1() == "value_1"
        assert j["r"]() == "yo"
        assert j.key_2.key_21[1][1]() == 2111

    def test_exception(self):
        j = loads(self.json1)
        with pytest.raises(JSaneException):
            j.key_2.nonexistent[0]()
        with pytest.raises(JSaneException):
            j.key_2.key_21[7]()
        with pytest.raises(JSaneException):
            j.key_2.nonexistent[0]()
        with pytest.raises(JSaneException):
            j.key_2.key_21[7]()
        with pytest.raises(JSaneException):
            j.key_1.key_2()
        with pytest.raises(IndexError):
            j.key_2.key_24.key_244.key_2442[0]()[7]
        with pytest.raises(JSaneException):
            j.key_2.key_24.key_244.key_2442[0][7]()

    def test_default(self):
        j = loads(self.json1)
        assert j.key_1.key_2(default=None) is None
        assert j.key_2.nonexistent[0](default="default") == "default"
        assert j.key_2.key_21[7](default="default") == "default"
        with pytest.raises(IndexError):
            j.key_2.key_24.key_244.key_2442[0](default="default")[7]

    def test_resolution(self):
        j = loads(self.json1)
        assert j.r() == "yo"
        assert j.key_2.key_21[0]() == [2100, 2101]
        assert j.key_2.key_21[0]() == [2100, 2101]
        assert j.key_2.key_24.key_244.key_2442[0]()[0] == "l"

    def test_numeric_resolution(self):
        j = loads(self.json1)
        assert +j.key_2.key_24.key_241 == 502
        assert +j.key_2.key_24.key_242[1][0] == 7
        assert +j.key_1 != +j.key_1  # inequality to oneself is the NaN test
        assert +j.nonexistent != +j.nonexistent
        assert +j.numeric_string != +j.numeric_string

    def test_easy_casting(self):
        j = loads(self.json1)
        assert str(j.key_2.key_21[0]) == "[2100, 2101]"
        assert str(j.numeric_string) == "115"
        assert int(j.numeric_string) == 115
        assert float(j.numeric_string) == 115.0
        assert type(float(j.numeric_string)) is float
        assert float(j.key_2.key_24.key_241) == 502
        assert type(float(j.key_2.key_24.key_241)) is float
        with pytest.raises(ValueError):
            int(j.key_1)
        with pytest.raises(ValueError):
            float(j.key_1)

    def test_contains(self):
        j = loads(self.json1)
        assert "key_1" in j
        assert "v" not in j.key_1  # do not pass 'in' operator to strings
        assert "v" in j.key_1()
        assert "key_22" in j.key_2
        assert "l1" in j.key_2.key_22  # do pass 'in' operator to lists
        assert "nonexistent" not in j

    def test_dir(self):
        j = loads(self.json1)
        assert "numeric_string" in dir(j)
        assert "key_22" in dir(j.key_2)
        with pytest.raises(JSaneException):
            dir(j.nonexistent)

    def test_setting(self):
        j = loads(self.json1)
        assert "nonexistent" not in j
        j.nonexistent = 5
        assert j.nonexistent() == 5
        del j.nonexistent
        assert "nonexistent" not in j
        j.list = [5]
        assert j.list[0]() == 5
        j.list[0] = "six"
        assert j.list[0]() == "six"

    def test_deleting(self):
        j = loads(self.json1)
        assert "r" in j
        del j.r
        assert "r" not in j
        assert j.list() == [1, 1, 2, 3, 5, 8]
        del j.list[1:-1]
        assert j.list() == [1, 8]

    def test_equality_behavior(self):
        i = loads('{"five": 5}')
        f = loads('{"five": 5.0}')
        assert i == f  # comparisons succeed between Traversable objects
        assert i.five == f.five
        assert i != {"five": 5}  # comparisons always return False otherwise
        assert i.five != 5
        assert i() == {"five": 5}
        assert i.five() == 5  # once the value is out, comparison succeeds

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

    def test_obj(self):
        obj = [1, 2, 3, {"foo": "bar"}]
        j = from_object(obj)
        assert j[0]() == 1
        for x, y in zip(j, obj):
            assert x() == y
        assert j[3].foo() == "bar"
