import os

env_file = os.getenv("GITHUB_ENV")

with open(env_file, "a") as myfile:
    myfile.write("TEST=Hello")
