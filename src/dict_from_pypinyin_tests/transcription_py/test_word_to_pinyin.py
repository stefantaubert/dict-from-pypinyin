from ordered_set import OrderedSet
from pytest import raises

from dict_from_pypinyin.transcription import Style, word_to_pinyin


def test_ABC():
  with raises(ValueError) as error:
    word_to_pinyin("ABC", style=Style.TONE, v_to_u=False)
  assert error.value.args[0] == "Syllable \"A\" couldn't be transcribed!"


def test_공():
  with raises(ValueError) as error:
    word_to_pinyin("공", style=Style.TONE, v_to_u=False)
  assert error.value.args[0] == "Syllable \"공\" couldn't be transcribed!"


def test_罷():
  result = word_to_pinyin("罷", style=Style.TONE, v_to_u=False)
  assert result == OrderedSet([('bà',), ('pí',), ('pì',), ('bǐ',), ('ba',), ('bǎi',)])


def test_罷罷():
  result = word_to_pinyin("罷罷", style=Style.TONE, v_to_u=False)
  assert result == OrderedSet([('bà', 'bà'), ('bà', 'pí'), ('bà', 'pì'), ('bà', 'bǐ'), ('bà', 'ba'), ('bà', 'bǎi'), ('pí', 'bà'), ('pí', 'pí'), ('pí', 'pì'), ('pí', 'bǐ'), ('pí', 'ba'), ('pí', 'bǎi'), ('pì', 'bà'), ('pì', 'pí'), ('pì', 'pì'), ('pì', 'bǐ'), ('pì', 'ba'), (
    'pì', 'bǎi'), ('bǐ', 'bà'), ('bǐ', 'pí'), ('bǐ', 'pì'), ('bǐ', 'bǐ'), ('bǐ', 'ba'), ('bǐ', 'bǎi'), ('ba', 'bà'), ('ba', 'pí'), ('ba', 'pì'), ('ba', 'bǐ'), ('ba', 'ba'), ('ba', 'bǎi'), ('bǎi', 'bà'), ('bǎi', 'pí'), ('bǎi', 'pì'), ('bǎi', 'bǐ'), ('bǎi', 'ba'), ('bǎi', 'bǎi')])
