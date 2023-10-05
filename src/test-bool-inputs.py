import os

env_var = os.environ.get("INPUT", True)

print(env_var, type(env_var))
