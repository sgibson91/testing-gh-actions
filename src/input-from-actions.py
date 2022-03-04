"""
Read in a list of files from the command line and echo the resulting parser, filepath
collection type, and the filepaths themselves
"""
import sys
import yaml
import argparse
import fnmatch
from pathlib import Path


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
filepaths = [Path(filepath).parent for filepath in args.filepaths]
cluster_filepaths = list(set(filepaths))
print(cluster_filepaths)

for cluster_filepath in cluster_filepaths:
    with open(cluster_filepath.joinpath("cluster.yaml")) as f:
        cluster_config = yaml.safe_load(f)

    cluster_info = {
        "cluster_name": cluster_config.get("name", {}),
        "provider": cluster_config.get("provider", {}),
    }

    for hub in cluster_config.get("hubs", {}):
        helm_chart_values_files = hub.get("helm_chart_values_files", {})

    print(cluster_info)
    print(helm_chart_values_files)
