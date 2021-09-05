from .cli.argparse import initialize_args
from .main import main as real_main
from .file_main import file_main
from .auth import auth
from .auth.auth_actions import get_follow_list
import sys

def main() :
    parser = initialize_args()
    args = parser.parse_args()
    if len(sys.argv) == 1 :
        parser.print_help()
    else :
        langwithindex = (args.language, args.index)
        if args.auth == False and args.follow_list == False and args.follow_list_download == False :
            if args.File == None :
                real_main(args.url, langwithindex, args.quality_mode, args.destination, args.max_threads, args.name, args.zip_name)
            else :
                file_main(args.File, langwithindex, args.quality_mode, args.destination, args.max_threads, args.zip_name)
        elif args.follow_list_download :
            token = auth()
            file = get_follow_list(token)
            file_main(file, langwithindex, args.quality_mode, args.destination, args.max_threads)
        elif args.follow_list :
            token = auth()
            get_follow_list(token)
        elif args.auth :
            auth()