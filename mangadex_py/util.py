from .cli.argparse import initialize_args
from .main import main as real_main

def main() :
    args = initialize_args().parse_args()
    print(args)

    langwithindex = (args.language, args.index)
    real_main(args.url, langwithindex, args.quality_mode, args.destination, args.max_threads)