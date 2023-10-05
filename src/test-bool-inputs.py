import os

env_var = eval(os.environ.get("INPUT", True))

print(env_var, type(env_var))
