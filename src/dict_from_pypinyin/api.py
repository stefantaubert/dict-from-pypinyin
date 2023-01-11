from typing import Tuple

from ordered_set import OrderedSet
from pypinyin import Style

from dict_from_pypinyin.transcription import word_to_pinyin as transcription_word_to_pinyin


def word_to_pinyin(word: str, style: Style, v_to_u: bool, strict: bool, neutral_tone_with_five: bool) -> OrderedSet[Tuple[str, ...]]:
  if not isinstance(word, str):
    raise ValueError("Parameter word: Value needs to be of type 'str'!")

  if " " in word:
    raise ValueError("Parameter word: Words containing space are not allowed!")

  if len(word.strip()) == 0:
    raise ValueError("Parameter word: Value must not be empty!")

  result = transcription_word_to_pinyin(word, style, v_to_u, strict, neutral_tone_with_five)
  return result
