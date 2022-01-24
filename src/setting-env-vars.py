import subprocess

subprocess.run([
    "echo", '"TEST=Hello"', ">>", "$GITHUB_ENV"
])
