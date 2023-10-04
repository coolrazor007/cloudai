# import sys
# import getopt


# def args(argv):
#     arg_audio = ""
#     #arg_output = ""
#     #arg_user = ""
#     arg_help = "{0} -a".format(argv[0])
    
#     try:
#         opts, args = getopt.getopt(argv[1:], "hi:u:o:", ["help", "audio="])
#     except:
#         print(arg_help)
#         sys.exit(2)
    
#     for opt, arg in opts:
#         if opt in ("-h", "--help"):
#             print(arg_help)  # print the help message
#             sys.exit(2)
#         elif opt in ("-a", "--audio"):
#             arg_audio = True
#         # elif opt in ("-u", "--user"):
#         #     arg_user = arg
#         # elif opt in ("-o", "--output"):
#         #     arg_output = arg

#     print('Audio:', 'enabled')
#     # print('user:', arg_user)
#     # print('output:', arg_output)

#     return(arg_audio)

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def args(argv):
    parser = ArgumentParser(description="Just an example", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--audio", action="store_true", help="audio enabled")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
    parser.add_argument("-s", "--slow", help="adds a sleep timer")
    parser.add_argument("-st", "--step", help="adds steps that require user intervention to continue")
    # parser.add_argument("--ignore-existing", action="store_true", help="skip files that exist")
    # parser.add_argument("--exclude", help="files to exclude")
    # parser.add_argument("src", help="Source location")
    # parser.add_argument("dest", help="Destination location")
    args = parser.parse_args()
    config = vars(args)
    print(config)
    return config