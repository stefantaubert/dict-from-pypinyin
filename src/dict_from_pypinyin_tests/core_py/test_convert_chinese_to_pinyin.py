from collections import OrderedDict

import pytest
from ordered_set import OrderedSet
from pypinyin import Style

from dict_from_pypinyin.core import convert_chinese_to_pinyin


def test_component():
  result, oov = convert_chinese_to_pinyin(OrderedSet([
    "罷",
    "罷.",
    "罷!",
    "有-罷",
    "㓛",
    "abc",
  ]), Style.TONE3, True, True, True, 0.5, {"."}, True, 1, None, 1)

  assert result == OrderedDict([('罷', OrderedDict([(('ba4',), 0.5), (('pi2',), 0.5), (('pi4',), 0.5), (('bi3',), 0.5), (('ba5',), 0.5), (('bai3',), 0.5)])), ('罷.', OrderedDict([(('ba4', '.'), 0.5), (('pi2', '.'), 0.5), (('pi4', '.'), 0.5), (('bi3', '.'), 0.5), (('ba5', '.'), 0.5), (('bai3', '.'), 0.5)])), ('有-罷', OrderedDict([(('you3', '-', 'ba4'), 0.25), (('you3', '-', 'pi2'), 0.25), (('you3', '-', 'pi4'), 0.25), (('you3', '-', 'bi3'), 0.25),
                               (('you3', '-', 'ba5'), 0.25), (('you3', '-', 'bai3'), 0.25), (('you4', '-', 'ba4'), 0.25), (('you4', '-', 'pi2'), 0.25), (('you4', '-', 'pi4'), 0.25), (('you4', '-', 'bi3'), 0.25), (('you4', '-', 'ba5'), 0.25), (('you4', '-', 'bai3'), 0.25), (('wei3', '-', 'ba4'), 0.25), (('wei3', '-', 'pi2'), 0.25), (('wei3', '-', 'pi4'), 0.25), (('wei3', '-', 'bi3'), 0.25), (('wei3', '-', 'ba5'), 0.25), (('wei3', '-', 'bai3'), 0.25)]))])
  assert oov == OrderedSet(['罷!', '㓛', 'abc'])


def test_wrong_format():
  with pytest.raises(ValueError) as error:
    convert_chinese_to_pinyin({"罷"})
  assert error.value.args[0] == "Value needs of type 'OrderedSet'!"


def test_wrong_style():
  with pytest.raises(ValueError) as error:
    convert_chinese_to_pinyin(OrderedSet({"罷"}), style=15)
  assert error.value.args[0] == 'Style not found!'


def test_empty():
  result, oov = convert_chinese_to_pinyin(OrderedSet())
  assert result == OrderedDict()
  assert oov == OrderedSet()
