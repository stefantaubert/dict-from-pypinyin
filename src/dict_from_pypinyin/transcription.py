import itertools
from typing import Tuple

from ordered_set import OrderedSet
from pypinyin import Style, pinyin


def word_to_pinyin(word: str, style: Style, v_to_u: bool, strict: bool, neutral_tone_with_five: bool) -> OrderedSet[Tuple[str, ...]]:
  assert isinstance(word, str)
  assert len(word) > 0

  syllables_pinyins = []
  for syllable in word:
    try:
      syllable_pinyins = pinyin(syllable, style=style, heteronym=True,
                                errors='ignore', strict=strict,
                                v_to_u=v_to_u, neutral_tone_with_five=neutral_tone_with_five)
    except ValueError as error:
      raise ValueError(f"Syllable \"{syllable}\" couldn't be transcribed!") from error
    except TypeError as error:
      raise ValueError(f"Syllable \"{syllable}\" couldn't be transcribed!") from error

    if len(syllable_pinyins) != 1 or len(syllable_pinyins[0]) == 0:
      raise ValueError(f"Syllable \"{syllable}\" couldn't be transcribed!")

    # if [syllable] == syllable_pinyins[0]:
    #   raise ValueError(f"Syllable \"{syllable}\" couldn't be transcribed!")

    # # e.g. [['㓛5']]
    # if style in {Style.TONE3, Style.BOPOMOFO} and syllable in syllable_pinyins[0][0]:
    #   raise ValueError(f"Syllable \"{syllable}\" couldn't be transcribed!")

    heteronyms = syllable_pinyins[0]
    syllables_pinyins.append(heteronyms)

  all_syllable_combinations = OrderedSet(
    combination
    for combination in itertools.product(*syllables_pinyins)
  )

  return all_syllable_combinations


# def word_to_pinyin_v2(word: str) -> OrderedSet[Tuple[str, ...]]:
#   assert isinstance(word, str)
#   assert len(word) > 0

#   syllables_pinyins = []

#   try:
#     syllables_pinyins = pinyin(word, style=Style.TONE, heteronym=True,
#                                errors='default', strict=True,
#                                v_to_u=False, neutral_tone_with_five=False)
#   except ValueError as error:
#     raise ValueError(f"Word \"{word}\" couldn't be transcribed!") from error

#   if len(syllables_pinyins) != len(word):
#     raise ValueError(f"Word \"{word}\" couldn't be transcribed!")

#   all_syllable_combinations = OrderedSet(
#     combination
#     for combination in itertools.product(*syllables_pinyins)
#   )

#   return all_syllable_combinations
