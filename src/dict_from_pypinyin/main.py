from argparse import ArgumentParser, Namespace
from logging import getLogger
from pathlib import Path
from tempfile import gettempdir

from ordered_set import OrderedSet
from pronunciation_dictionary import SerializationOptions, save_dict
from pypinyin import Style

from dict_from_pypinyin.argparse_helper import (DEFAULT_PUNCTUATION, ConvertToOrderedSetAction,
                                                EnumAction, add_chunksize_argument,
                                                add_encoding_argument, add_maxtaskperchild_argument,
                                                add_n_jobs_argument, add_serialization_group,
                                                get_optional, parse_existing_file,
                                                parse_non_empty_or_whitespace, parse_path,
                                                parse_positive_float)
from dict_from_pypinyin.core import convert_chinese_to_pinyin


def get_app_try_add_vocabulary_from_pronunciations_parser(parser: ArgumentParser):
  parser.description = "Command-line interface (CLI) to create a pronunciation dictionary by looking up IPA transcriptions using pypinyin including the possibility of ignoring punctuation and splitting words on hyphens before transcribing them."
  default_oov_out = Path(gettempdir()) / "oov.txt"
  # TODO support multiple files
  parser.add_argument("vocabulary", metavar='VOCABULARY-PATH', type=parse_existing_file,
                      help="file containing the vocabulary (words separated by line)")
  add_encoding_argument(parser, "--vocabulary-encoding", "encoding of vocabulary")
  parser.add_argument("dictionary", metavar='DICTIONARY-PATH', type=parse_path,
                      help="path to output the created dictionary")
  parser.add_argument("--weight", type=parse_positive_float, metavar="WEIGHT",
                      help="weight to assign for each pronunciation", default=1.0)
  parser.add_argument("--trim", type=parse_non_empty_or_whitespace, metavar='TRIM-SYMBOL', nargs='*',
                      help="trim these symbols from the start and end of a word before lookup", action=ConvertToOrderedSetAction, default=DEFAULT_PUNCTUATION)
  parser.add_argument("--split-on-hyphen", action="store_true",
                      help="split words on hyphen symbol before lookup")
  parser.add_argument("--style", type=Style, default=Style.TONE,
                      action=EnumAction, help="pinyin style")
  parser.add_argument("--ü-to-v", action="store_true",
                      help="whether to use `v` instead of `ü` (applicable if Style is not 'TONE'); default behavior: use `ü`")
  parser.add_argument("--non-strict", action="store_true",
                      help="don't use strict transcription")
  parser.add_argument("--neutral-tone-with-five", action="store_true",
                      help="transcribe neutral tone with 5 in Styles TONE2/TONE3")
  parser.add_argument("--oov-out", metavar="OOV-PATH", type=get_optional(parse_path),
                      help="write out-of-vocabulary (OOV) words (i.e., words that can't transcribed) to this file (encoding will be the same as the one from the vocabulary file)", default=default_oov_out)
  add_serialization_group(parser)
  mp_group = parser.add_argument_group("multiprocessing arguments")
  add_n_jobs_argument(mp_group)
  add_chunksize_argument(mp_group)
  add_maxtaskperchild_argument(mp_group)
  return get_pronunciations_files


def get_pronunciations_files(ns: Namespace) -> bool:
  assert ns.vocabulary.is_file()
  logger = getLogger(__name__)

  try:
    vocabulary_content = ns.vocabulary.read_text(ns.vocabulary_encoding)
  except Exception as ex:
    logger.error("Vocabulary couldn't be read.")
    return False

  vocabulary_words = OrderedSet(vocabulary_content.splitlines())
  strict = not ns.non_strict
  v_to_u = not ns.ü_to_v

  dictionary_instance, unresolved_words = convert_chinese_to_pinyin(
    vocabulary_words, ns.style, v_to_u, strict, ns.neutral_tone_with_five, ns.weight, ns.trim, ns.split_on_hyphen, ns.n_jobs, ns.maxtasksperchild, ns.chunksize, silent=False)

  s_options = SerializationOptions(ns.parts_sep, ns.include_numbers, ns.include_weights)

  try:
    save_dict(dictionary_instance, ns.dictionary, ns.serialization_encoding, s_options)
  except Exception as ex:
    logger.error("Dictionary couldn't be written.")
    logger.debug(ex)
    return False

  logger.info(f"Written dictionary to: \"{ns.dictionary.absolute()}\".")

  if len(unresolved_words) > 0:
    logger.warning("Not all words could be transcribed to pinyin!")
    if ns.oov_out is not None:
      unresolved_out_content = "\n".join(unresolved_words)
      ns.oov_out.parent.mkdir(parents=True, exist_ok=True)
      try:
        ns.oov_out.write_text(unresolved_out_content, "UTF-8")
      except Exception as ex:
        logger.error("Unresolved output file couldn't be created!")
        return False
      logger.info(f"Written unresolved vocabulary to: \"{ns.oov_out.absolute()}\".")
  else:
    logger.info("Complete vocabulary is contained in output!")

  return True

