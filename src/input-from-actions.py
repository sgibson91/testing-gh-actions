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

# Filter for all target files
all_target_files = []
patterns_to_match = ["*/cluster.yaml", "*/*.values.yaml"]  #, "*/support.values.yaml"]

for pattern in patterns_to_match:
    all_target_files.extend(fnmatch.filter(args.filepaths, pattern))

# Filter for values files
values_files = set(fnmatch.filter(args.filepaths, "*/*.values.yaml"))

# Identify unique cluster paths amongst target paths
cluster_filepaths = list(set([Path(filepath).parent for filepath in all_target_files]))

matrix_jobs = []
for cluster_filepath in cluster_filepaths:
    with open(cluster_filepath.joinpath("cluster.yaml")) as f:
        cluster_config = yaml.safe_load(f)

    cluster_info = {
        "cluster_name": cluster_config.get("name", {}),
        "provider": cluster_config.get("provider", {}),
    }

    for hub in cluster_config.get("hubs", {}):
        helm_chart_values_files = [str(cluster_filepath.joinpath(values_file)) for values_file in hub.get("helm_chart_values_files", {})]
        intersection_of_input_files_and_helm_values_files = list(values_files.intersection(helm_chart_values_files))

        if len(intersection_of_input_files_and_helm_values_files) > 0:
            new_entry = cluster_info.copy()
            new_entry["hub_name"] = hub["name"]
            matrix_jobs.append(new_entry)

print("Matrix jobs:" matrix_jobs)
