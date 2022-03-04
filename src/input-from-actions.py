"""
Read in a list of files from the command line and echo the resulting parser, filepath
collection type, and the filepaths themselves
"""
import os
import yaml
import argparse
import fnmatch
from pathlib import Path


def convert_string_to_list(full_str):
    return full_str.split(" ")


def generate_lists_of_filepaths_and_filenames(input_file_list):
    patterns_to_match = ["*/cluster.yaml", "*/*.values.yaml"]  #, "*/support.values.yaml"]
    all_target_files = []

    # Filter for all targeted files
    for pattern in patterns_to_match:
        all_target_files.extend(fnmatch.filter(input_file_list, pattern))

    # Identify unique cluster paths amongst target paths
    cluster_filepaths = list(set([Path(filepath).parent for filepath in all_target_files]))

    # Filter for all values files
    values_files = set(fnmatch.filter(input_file_list, "*/*.values.yaml"))

    return cluster_filepaths, values_files


def generate_basic_cluster_info(cluster_name, provider, needs=[]):
    cluster_info = {
        "cluster_name": cluster_name,
        "provider": provider,
        "needs": [],
    }

    return cluster_info


def generate_hub_matrix_jobs(cluster_filepaths, values_files):
    matrix_jobs = []
    for cluster_filepath in cluster_filepaths:
        with open(cluster_filepath.joinpath("cluster.yaml")) as f:
            cluster_config = yaml.safe_load(f)

        cluster_info = generate_basic_cluster_info(cluster_config.get("name", {}), cluster_config.get("provider", {}))

        for hub in cluster_config.get("hubs", {}):
            helm_chart_values_files = [str(cluster_filepath.joinpath(values_file)) for values_file in hub.get("helm_chart_values_files", {})]
            intersection = list(values_files.intersection(helm_chart_values_files))

            if len(intersection) > 0:
                new_entry = cluster_info.copy()
                new_entry["hub_name"] = hub["name"]
                matrix_jobs.append(new_entry)

    return matrix_jobs


def update_github_env(hub_matrix_jobs):
    with open(os.getenv("GITHUB_ENV"), "a") as f:
        f.write(f"HUB_MATRIX_JOBS={hub_matrix_jobs}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "filepaths",
        nargs="?",
        type=convert_string_to_list,
        help="A singular or space-delimited list of newly added or modified filepaths in the repo"
    )

    args = parser.parse_args()

    cluster_filepaths, values_files = generate_lists_of_filepaths_and_filenames(args.filepaths)
    hub_matrix_jobs = generate_hub_matrix_jobs(cluster_filepaths, values_files)
    update_github_env(hub_matrix_jobs)


if __name__ == "__main__":
    main()
