from pathlib import Path

from ordered_set import OrderedSet
from pytest import raises
from tqdm import tqdm

from dict_from_pypinyin.transcription import Style, word_to_pinyin


def test_non_hanzi_ABC__raises_value_error():
  with raises(ValueError) as error:
    word_to_pinyin("ABC", style=Style.TONE, v_to_u=False, strict=True, neutral_tone_with_five=True)
  assert error.value.args[0] == "Syllable \"A\" couldn't be transcribed!"


def test_誒__is_correctly_transcribed():
  # in V 0.47.1 this was a bug
  res = word_to_pinyin("誒", style=Style.BOPOMOFO, v_to_u=False,
                       strict=True, neutral_tone_with_five=True)
  # assert res == OrderedSet([('ㄟˊ',), ('ㄒㄧ',), ('ㄧˋ',), ('ê',), ('êˊ',),('êˇ',), ('ㄟˇ',), ('êˋ',), ('ㄟˋ',), ('ㄟ',)])
  assert res == OrderedSet([('ㄟˊ',), ('ㄒㄧ',), ('ㄧˋ',), ('ㄝ',), ('ㄝˊ',),
                           ('ㄝˇ',), ('ㄟˇ',), ('ㄝˋ',), ('ㄟˋ',), ('ㄟ',)])


def test_欸__is_correctly_transcribed():
  # in V 0.47.1 this was a bug
  res = word_to_pinyin("欸", style=Style.BOPOMOFO, v_to_u=False,
                       strict=True, neutral_tone_with_five=True)
  # assert res == OrderedSet([('ㄞ',), ('ㄞˇ',), ('ê',), ('êˊ',), ('êˇ',),('êˋ',), ('ㄒㄧㄝˋ',), ('ㄟˊ',), ('ㄟˇ',), ('ㄟˋ',), ('ㄟ',)])
  assert res == OrderedSet([('ㄞ',), ('ㄞˇ',), ('ㄝ',), ('ㄝˊ',), ('ㄝˇ',),
                           ('ㄝˋ',), ('ㄒㄧㄝˋ',), ('ㄟˊ',), ('ㄟˇ',), ('ㄟˋ',), ('ㄟ',)])


def test_㓛_tone2__raises_value_error_from_type_error():
  with raises(ValueError) as error:
    word_to_pinyin("㓛", style=Style.TONE2, v_to_u=False, strict=True, neutral_tone_with_five=True)
  assert error.value.args[0] == "Syllable \"㓛\" couldn't be transcribed!"


def test_㓛_tone3__raises_value_error_from_type_error():
  with raises(ValueError) as error:
    word_to_pinyin("㓛", style=Style.TONE3, v_to_u=False, strict=True, neutral_tone_with_five=True)
  assert error.value.args[0] == "Syllable \"㓛\" couldn't be transcribed!"


def test_㓛_bopomofo__raises_value_error_from_type_error():
  with raises(ValueError) as error:
    word_to_pinyin("㓛", style=Style.BOPOMOFO, v_to_u=False,
                   strict=True, neutral_tone_with_five=True)
  assert error.value.args[0] == "Syllable \"㓛\" couldn't be transcribed!"


def test_㓛_bopomofo_first__raises_value_error_from_type_error():
  with raises(ValueError) as error:
    word_to_pinyin("㓛", style=Style.BOPOMOFO_FIRST, v_to_u=False,
                   strict=True, neutral_tone_with_five=True)
  assert error.value.args[0] == "Syllable \"㓛\" couldn't be transcribed!"


def test_㓛_cyrillic__raises_value_error_from_type_error():
  with raises(ValueError) as error:
    word_to_pinyin("㓛", style=Style.CYRILLIC, v_to_u=False,
                   strict=True, neutral_tone_with_five=True)
  assert error.value.args[0] == "Syllable \"㓛\" couldn't be transcribed!"


def test_㓛_wadegiles__raises_value_error_from_type_error():
  with raises(ValueError) as error:
    word_to_pinyin("㓛", style=Style.WADEGILES, v_to_u=False,
                   strict=True, neutral_tone_with_five=True)
  assert error.value.args[0] == "Syllable \"㓛\" couldn't be transcribed!"


def test_공__raises_value_error():
  with raises(ValueError) as error:
    word_to_pinyin("공", style=Style.TONE, v_to_u=False, strict=True, neutral_tone_with_five=True)
  assert error.value.args[0] == "Syllable \"공\" couldn't be transcribed!"


def test_罷():
  result = word_to_pinyin("罷", style=Style.TONE, v_to_u=False,
                          strict=True, neutral_tone_with_five=True)
  assert result == OrderedSet([('bà',), ('pí',), ('pì',), ('bǐ',), ('ba',), ('bǎi',)])


def test_罷罷():
  result = word_to_pinyin("罷罷", style=Style.TONE, v_to_u=False,
                          strict=True, neutral_tone_with_five=True)
  assert result == OrderedSet([('bà', 'bà'), ('bà', 'pí'), ('bà', 'pì'), ('bà', 'bǐ'), ('bà', 'ba'), ('bà', 'bǎi'), ('pí', 'bà'), ('pí', 'pí'), ('pí', 'pì'), ('pí', 'bǐ'), ('pí', 'ba'), ('pí', 'bǎi'), ('pì', 'bà'), ('pì', 'pí'), ('pì', 'pì'), ('pì', 'bǐ'), ('pì', 'ba'), (
    'pì', 'bǎi'), ('bǐ', 'bà'), ('bǐ', 'pí'), ('bǐ', 'pì'), ('bǐ', 'bǐ'), ('bǐ', 'ba'), ('bǐ', 'bǎi'), ('ba', 'bà'), ('ba', 'pí'), ('ba', 'pì'), ('ba', 'bǐ'), ('ba', 'ba'), ('ba', 'bǎi'), ('bǎi', 'bà'), ('bǎi', 'pí'), ('bǎi', 'pì'), ('bǎi', 'bǐ'), ('bǎi', 'ba'), ('bǎi', 'bǎi')])


def test_vocabulary__everything_could_be_transcribed_in_all_relevant_styles():
  voc = Path("res/hanzi-syllables.txt").read_text("UTF-8")
  syllables = voc.splitlines()
  result = []
  failed = OrderedSet()
  for syllable in tqdm(syllables):
    transcripts = []
    try:
      transcripts.append(word_to_pinyin(syllable, Style.NORMAL, True, True, True))
      transcripts.append(word_to_pinyin(syllable, Style.TONE, True, True, True))
      transcripts.append(word_to_pinyin(syllable, Style.TONE2, True, True, True))
      transcripts.append(word_to_pinyin(syllable, Style.TONE3, True, True, True))
      transcripts.append(word_to_pinyin(syllable, Style.BOPOMOFO, True, True, True))
      transcripts.append(word_to_pinyin(syllable, Style.CYRILLIC, True, True, True))
      transcripts.append(word_to_pinyin(syllable, Style.WADEGILES, True, True, True))
    except ValueError as error:
      failed.add(syllable)
    result.append((syllable, transcripts))
  assert len(result) == len(syllables)
