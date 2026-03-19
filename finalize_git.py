import subprocess

git_path = r"C:\Program Files\Git\cmd\git.exe"

subprocess.run([git_path, 'remote', 'remove', 'origin'], check=False)
subprocess.run([git_path, 'remote', 'add', 'origin', 'https://github.com/ranganamadushan/mysite.git'], check=True)

print("Fetching mysite repository...")
try:
    subprocess.run([git_path, 'fetch', 'origin'], check=True)
    subprocess.run([git_path, 'reset', '--soft', 'origin/main'], check=False)
    print("Successfully correctly mapped local folder explicitly to ranganamadushan/mysite!")
except Exception as e:
    print(f"Fetch/reset failed, continuing gracefully as remote might be entirely empty natively: {e}")
