import os
import subprocess

locks = [r'g:\My Drive\MYSITE\.git\config.lock', r'g:\My Drive\MYSITE\.git\HEAD.lock']
for lock in locks:
    if os.path.exists(lock):
        try:
            os.remove(lock)
            print(f"Successfully removed stuck git lock: {lock}")
        except Exception as e:
            print(f"Could not remove {lock}, error: {e}")

print("Running Git initialization script...")
subprocess.run(['python', 'setup_git.py'])

print("\nRunning Main Portfolio Engine to test Auto-Deploy...")
subprocess.run(['python', 'update_portfolio.py'])
