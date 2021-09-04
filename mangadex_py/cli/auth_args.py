def _auth_args(args_parser) :
    args = args_parser.add_argument_group("Auth related options")
    args.add_argument(
        "-A",
        "--auth",
        action="store_true",
        default=False,
        help=(
            "i.e initialize authentication, will use the .dex to authenticate."
        )
    )
    args.add_argument(
        "-fl",
        "--follow-list",
        action="store_true",
        default=False,
        help=(
            "i.e create manga follow list in the current working dir 'follow.list'."
        )
    )
    args.add_argument(
        "-fldl",
        "--follow-list-download",
        action="store_true",
        default=False,
        help=(
            "i.e Download manga follow list from 'follow.list'."
        )
    )