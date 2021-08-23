from argparse import ArgumentParser

#https://github.com/manga-py/manga-py/blob/d89501a0f78d498f85114320d6123f59d328a905/manga_py/cli/_args_general.py#L4
def _gen_args(args_parser: ArgumentParser, version) :
    args = args_parser.add_argument_group('General options')
    args.add_argument(
        'url',
        metavar='URL',
        type=str,
        help=(
            '%(metavar)s, i.e. link for the manga to be downloaded.'
        )
    )
    args.add_argument(
        '-v',
        '--version',
        action='version',
        version=version,
        help=(
            'Show %(prog)s\'s version number and exit.'
        )
    )
    args.add_argument(
        '-d',
        '--destination',
        metavar='PATH',
        type=str,
        default='Manga',
        help=(
            'Destination folder to where the manga will be saved locally. '
            'The path will be `./%(metavar)s/manga_name/`.'
        )
    )
    args.add_argument(
        '-F', 
        '--File',
        metavar='FILE',
        type=str,
        help=(
            '%(metavar)s, i.e. folder containing the links for the mangas to be downloaded.'
        )
    )