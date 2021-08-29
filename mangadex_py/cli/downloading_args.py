#https://github.com/manga-py/manga-py/blob/d89501a0f78d498f85114320d6123f59d328a905/manga_py/cli/_args_downloading.py#L2
def _download_args(args_parser) :
    args = args_parser.add_argument_group('Downloading options')
    args.add_argument(
        '-t',
        '--max-threads',
        type=int,
        metavar="thread",
        default=0,
        help=(
            'Set the maximum number of threads, i.e. MAX_THREADS, to be avaliable to mangadex-py. '
            'Threads run in pseudo-parallel when execute the process to download the manga images.'
        )
    )
    args.add_argument(
        '-l',
        '--language',
        type=str,
        metavar="lang",
        default="en",
        help=(
            'Set the language in which the chapters should be downloaded. '
        )
    )
    args.add_argument(
        '-n',
        '--index',
        type=int,
        metavar="index",
        default=0,
        help=(
            'Sometimes there could be more than 1 altTitles in the desired lanuguage this will let you control which one to choose. '
        )
    )
    args.add_argument(
        '-ds',
        '--quality-mode',
        type=str,
        metavar="quality_mode",
        default="data",
        help=(
            'change the quality mode from data to dataSaver. '
            'data-saver will download a compressed image instead of upload quality.'
        )
    )
    args.add_argument(
        '--name',
        type=str,
        metavar="name",
        default=None,
        help=(
            'set a custom manga name for the folder and everything else. '
        )
    )