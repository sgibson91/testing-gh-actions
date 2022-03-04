"""
Read in a list of files from the command line and echo the resulting parser, filepath
collection type, and the filepaths themselves
"""
import os
import sys
import yaml
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

# Filter for target files
target_files = []
patterns_to_match = ["*/cluster.yaml", "*/*.values.yaml"]  #, "*/support.values.yaml"]

for pattern in patterns_to_match:
    target_files.extend(fnmatch.filter(args.filepaths, pattern))

# Identify unique cluster paths amongst target paths
filepaths = [os.path.dirname(filepath) for filepath in args.filepaths]
cluster_filepaths = list(set(filepaths))
print(cluster_filepaths)

# clusters = []
# # Grab all cluster names from changed values names. This is in case a values file is
# # added/modified but not the associated cluster.yaml file.
# for values_file in values_files:
#     cluster = os.path.basename(os.path.dirname(values_file))
#     if cluster not in clusters:
#         clusters.append(cluster)
# # Now check all added/modified cluster files incase we've missed one
# for cluster_file in cluster_files:
#     with open(cluster_file) as f:
#         cluster = yaml.safe_load(f)
#     if cluster["name"] not in clusters:
#         clusters.append(cluster["name"])

# print(clusters)
