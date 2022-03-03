"""
Read in a list of files from the command line and echo the resulting parser, filepath
collection type, and the filepaths themselves
"""
import sys
import argparse
import fnmatch


def convert_string_to_list(full_str):
    return full_str.split(" ")


parser = argparse.ArgumentParser()

parser.add_argument(
    "filepaths",
    nargs="?",
    type=convert_string_to_list,
    help="A singular or space-delimited list of newly added or modified filepaths in the repo"
)

args = parser.parse_args()

# Filter for cluster.yaml files
cluster_files = fnmatch.filter(args.filepaths, "*/cluster.yaml")
# Filter for *.values.yaml files
values_files = fnmatch.filter(args.filepaths, "*/*.values.yaml")
# Filter for support.values.yaml files
support_files = fnmatch.filter(args.filepaths, "*/support.values.yaml")

if not cluster_files and not values_files and not support_files:
    print("Nothing to do!")
    sys.exit()
