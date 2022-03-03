"""
Read in a list of files from the command line and echo the resulting parser, filepath
collection type, and the filepaths themselves
"""
import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "filepaths",
    nargs="?",
    help="A singular or list of newly added or modified filepaths in the repo"
)

args = parser.parse_args()

print(vars(args))
print(type(args.filepaths))
print(args.filepaths)
