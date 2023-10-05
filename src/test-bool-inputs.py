import os

env_var = eval(os.environ.get("INPUT", "true").capitalize())

print(env_var, type(env_var))
