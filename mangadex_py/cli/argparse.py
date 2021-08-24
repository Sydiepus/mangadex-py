from argparse import ArgumentParser
from mangadex_py.meta import version
from .general_args import _gen_args
from .downloading_args import _download_args
from .required_args import _required_args


def initialize_args() -> ArgumentParser :
    args_parser = ArgumentParser(
        prog="mangadex-py",
        description=(
            '%(prog)s is the MangaDexv5 manga downloader.\n  '
           'Source-code: https://github.com/Sydiepus/mangadex-py\n  '
            'Version: ' + version
        )
    )
    _required_args(args_parser)
    _gen_args(args_parser, version)
    _download_args(args_parser)
    return args_parser