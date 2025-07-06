import subprocess

def clone_repo(url, target_dir):
    subprocess.run(["git", "clone", url, target_dir]) 