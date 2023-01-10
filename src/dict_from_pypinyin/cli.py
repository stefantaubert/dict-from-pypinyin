import argparse
import logging
import sys
from argparse import ArgumentParser
from importlib.metadata import version
from logging import getLogger
from pathlib import Path
from tempfile import gettempdir
from typing import Callable, Generator, List, Tuple

from dict_from_pypinyin.logging_configuration import configure_root_logger
from dict_from_pypinyin.main import get_app_try_add_vocabulary_from_pronunciations_parser

PROG_NAME = "dict-from-pypinyin"
__version__ = version(PROG_NAME)

INVOKE_HANDLER_VAR = "invoke_handler"


Parsers = Generator[Tuple[str, str, Callable], None, None]


def formatter(prog):
  return argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=40)


def _init_parser():
  main_parser = ArgumentParser(formatter_class=formatter)
  main_parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
  method = get_app_try_add_vocabulary_from_pronunciations_parser(main_parser)
  main_parser.set_defaults(**{
      INVOKE_HANDLER_VAR: method,
  })

  return main_parser


def configure_logger(productive: bool) -> None:
  loglevel = logging.INFO if productive else logging.DEBUG
  main_logger = getLogger()
  main_logger.setLevel(loglevel)
  main_logger.manager.disable = logging.NOTSET
  if len(main_logger.handlers) > 0:
    console = main_logger.handlers[0]
  else:
    console = logging.StreamHandler()
    main_logger.addHandler(console)

  logging_formatter = logging.Formatter(
    '[%(asctime)s.%(msecs)03d] (%(levelname)s) %(message)s',
    '%Y/%m/%d %H:%M:%S',
  )
  console.setFormatter(logging_formatter)
  console.setLevel(loglevel)


def parse_args(args: List[str]):
  configure_root_logger()

  root_logger = getLogger()

  local_debugging = debug_file_exists()
  if local_debugging:
    root_logger.debug(f"Received arguments: {str(args)}")

  parser = _init_parser()

  if len(args) == 0:
    parser.print_help()
    return

  received_args = parser.parse_args(args)

  if local_debugging:
    root_logger.debug(f"Parsed arguments: {str(received_args)}")

  params = vars(received_args)

  if INVOKE_HANDLER_VAR in params:
    invoke_handler: Callable[[ArgumentParser], None] = params.pop(INVOKE_HANDLER_VAR)
    invoke_handler(received_args)
  else:
    parser.print_help()


def debug_file_exists():
  return (Path(gettempdir()) / f"{PROG_NAME}-debug").is_file()


def create_debug_file():
  if not debug_file_exists():
    (Path(gettempdir()) / f"{PROG_NAME}-debug").write_text("", "UTF-8")


def run():
  arguments = sys.argv[1:]
  parse_args(arguments)


def run_prod():
  run()


if __name__ == "__main__":
  run_prod()
