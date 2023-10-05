import os

env_var = bool(os.environ.get("INPUT", True))

print(env_var, type(env_var))
