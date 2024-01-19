
from argparse import ArgumentParser, Namespace
from dict_from_pypinyin.transcription import word_to_pinyin
from dict_from_pypinyin.argparse_helper import (DEFAULT_PUNCTUATION, ConvertToOrderedSetAction,
                                                EnumAction, add_chunksize_argument,
                                                add_encoding_argument, add_maxtaskperchild_argument,
                                                add_n_jobs_argument, add_serialization_group,
                                                get_optional, parse_existing_file,
                                                parse_non_empty_or_whitespace, parse_path,
                                                parse_positive_float)
from word_to_pronunciation import Options, get_pronunciations_from_word
from tqdm import tqdm
from pypinyin import Style
from pronunciation_dictionary import (PronunciationDict, Pronunciations, SerializationOptions, Word,
                                      save_dict)
from ordered_set import OrderedSet
from typing import Dict, Optional, Set, Tuple
from tempfile import gettempdir
from pathlib import Path
from multiprocessing.pool import Pool
from logging import getLogger
from functools import partial
from collections import OrderedDict


def convert_chinese_to_pinyin(vocabulary: OrderedSet[Word], style: Style, v_to_u: bool, strict: bool, neutral_tone_with_five: bool, weight: float,
                              trim_symbols: Set[str], split_on_hyphen: bool, n_jobs: int, maxtasksperchild: Optional[int], chunksize: int, silent: bool = True) -> Tuple[PronunciationDict, OrderedSet[Word]]:
  trim = ''.join(trim_symbols)
  options = Options(trim, split_on_hyphen, False, False, weight)

  dictionary_instance, unresolved_words = get_pronunciations(
    vocabulary, style, v_to_u, strict, neutral_tone_with_five, weight, options, n_jobs, maxtasksperchild, chunksize, silent)
  return dictionary_instance, unresolved_words


def get_pronunciations(vocabulary: OrderedSet[Word], style: Style, v_to_u: bool, strict: bool, neutral_tone_with_five: bool, weight: float, options: Options, n_jobs: int, maxtasksperchild: Optional[int], chunksize: int, silent: bool) -> Tuple[PronunciationDict, OrderedSet[Word]]:
  lookup_method = partial(
    process_get_pronunciation,
    weight=weight,
    style=style,
    v_to_u=v_to_u,
    strict=strict,
    neutral_tone_with_five=neutral_tone_with_five,
    options=options,
  )

  with Pool(
    processes=n_jobs,
    initializer=__init_pool_prepare_cache_mp,
    initargs=(vocabulary,),
    maxtasksperchild=maxtasksperchild,
  ) as pool:
    entries = range(len(vocabulary))
    iterator = pool.imap(lookup_method, entries, chunksize)
    pronunciations_to_i = dict(tqdm(iterator, total=len(entries), unit="words", disable=silent))

  return get_dictionary(pronunciations_to_i, vocabulary)


def get_dictionary(pronunciations_to_i: Dict[int, Pronunciations], vocabulary: OrderedSet[Word]) -> Tuple[PronunciationDict, OrderedSet[Word]]:
  resulting_dict = OrderedDict()
  unresolved_words = OrderedSet()

  for i, word in enumerate(vocabulary):
    pronunciations = pronunciations_to_i[i]

    if len(pronunciations) == 0:
      unresolved_words.add(word)
      continue
    assert word not in resulting_dict
    resulting_dict[word] = pronunciations

  return resulting_dict, unresolved_words


process_unique_words: OrderedSet[Word] = None


def __init_pool_prepare_cache_mp(words: OrderedSet[Word]) -> None:
  global process_unique_words
  process_unique_words = words


def process_get_pronunciation(word_i: int, style: Style, v_to_u: bool, strict: bool, neutral_tone_with_five: bool, weight: float, options: Options) -> Tuple[int, Pronunciations]:
  global process_unique_words
  assert 0 <= word_i < len(process_unique_words)
  word = process_unique_words[word_i]

  # TODO support all entries; also create all combinations with hyphen then
  lookup_method = partial(
    lookup_in_model,
    style=style,
    v_to_u=v_to_u,
    strict=strict,
    neutral_tone_with_five=neutral_tone_with_five,
    weight=weight,
  )

  pronunciations = get_pronunciations_from_word(word, lookup_method, options)
  # logger = getLogger(__name__)
  # logger.debug(pronunciations)
  return word_i, pronunciations


def lookup_in_model(word: Word, style: Style, v_to_u: bool, strict: bool, neutral_tone_with_five: bool, weight: float) -> Pronunciations:
  assert len(word) > 0
  try:
    word_pinyins = word_to_pinyin(word, style, v_to_u, strict, neutral_tone_with_five)
  except ValueError as error:
    return OrderedDict()
  except TypeError as error:
    return OrderedDict()

  result = OrderedDict(
    (word_IPA, weight)
    for word_IPA in word_pinyins
  )
  return result
