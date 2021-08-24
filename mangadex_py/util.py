from .cli.argparse import initialize_args
from .main import main as real_main
from .file_main import file_main

def main() :
    args = initialize_args().parse_args()
    print(args)

    langwithindex = (args.language, args.index)
    if args.File == None :
        real_main(args.url, langwithindex, args.quality_mode, args.destination, args.max_threads, args.name)
    else :
        file_main(args.File, langwithindex, args.quality_mode, args.destination, args.max_threads)