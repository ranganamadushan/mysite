import subprocess
import urllib.request
import json
import os

git_path = r"C:\Program Files\Git\cmd\git.exe"
os.chdir(r"g:\My Drive\MYSITE")

print("Initializing local repository...")
subprocess.run([git_path, 'init'], check=True)

default_branch = "main"
try:
    print("Detecting remote branch format...")
    resp = urllib.request.urlopen("https://api.github.com/repos/ranganamadushan/ranganamadushan.github.io")
    repo_info = json.loads(resp.read())
    default_branch = repo_info.get("default_branch", "main")
except Exception as e:
    print(f"Could not reach GitHub API: {e}")

print("Adding remote origin...")
# If origin already exists, this might fail, so we ignore errors silently
subprocess.run([git_path, 'remote', 'add', 'origin', 'https://github.com/ranganamadushan/ranganamadushan.github.io.git'], check=False, capture_output=True)

print("Fetching from remote...")
subprocess.run([git_path, 'fetch', 'origin'], check=False)

print(f"Setting active branch to {default_branch}...")
subprocess.run([git_path, 'branch', '-M', default_branch], check=False)

print("Synchronizing local files with remote history...")
try:
    subprocess.run([git_path, 'reset', '--soft', f'origin/{default_branch}'], check=True)
    print("Git repository configured successfully!")
except subprocess.CalledProcessError:
    print("Repository synchronization complete (fresh initialization).")
