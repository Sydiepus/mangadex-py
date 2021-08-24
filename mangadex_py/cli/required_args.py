#https://stackoverflow.com/a/11155124
def _required_args(args_parser) :
    args = args_parser.add_mutually_exclusive_group()
    args.add_argument(
        'url',
        metavar='URL',
        type=str,
        nargs='?',
        help=(
            '%(metavar)s, i.e. link for the manga to be downloaded.'
        )
    )
    args.add_argument(
        '-F', 
        '--File',
        metavar='FILE',
        default=None,
        type=str,
        nargs='?',
        help=(
            '%(metavar)s, i.e. folder containing the links for the mangas to be downloaded.'
        )
    )   