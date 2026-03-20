import os
import shutil

os.chdir(r"G:\My Drive\MYSITE")

os.makedirs('pages', exist_ok=True)
os.makedirs('assets/css', exist_ok=True)
os.makedirs('assets/js', exist_ok=True)
os.makedirs('assets/images', exist_ok=True)
os.makedirs('engine', exist_ok=True)

junk = ['CV - SDSU.pdf', 'extract_test.py', 'profile.txt', 'clean.py', 'add_moodle.py', 'add_research.py', 'add_visits.py', 'build_apps_page.py', 'update_eis.py', 'add_ga.py', 'setup_git.py', 'fix_git.py', 'finalize_git.py', 'test_doi.py']
for j in junk:
    if os.path.exists(j): os.remove(j)

if os.path.exists('style.css'): shutil.move('style.css', 'assets/css/style.css')
if os.path.exists('script.js'): shutil.move('script.js', 'assets/js/script.js')
if os.path.exists('IMG-20260228-WA0205.jpg'): shutil.move('IMG-20260228-WA0205.jpg', 'assets/images/IMG-20260228-WA0205.jpg')

html_files = ['education.html', 'experience.html', 'projects.html', 'applications.html', 'publications.html']
for h in html_files:
    if os.path.exists(h): shutil.move(h, f'pages/{h}')

if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f: idx = f.read()
    idx = idx.replace('href="style.css"', 'href="assets/css/style.css"')
    idx = idx.replace('src="script.js"', 'src="assets/js/script.js"')
    idx = idx.replace('src="IMG-20260228-WA0205.jpg"', 'src="assets/images/IMG-20260228-WA0205.jpg"')
    for h in html_files: idx = idx.replace(f'href="{h}"', f'href="pages/{h}"')
    with open('index.html', 'w', encoding='utf-8') as f: f.write(idx)

for h in html_files:
    path = f'pages/{h}'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f: pg = f.read()
        pg = pg.replace('href="style.css"', 'href="../assets/css/style.css"')
        pg = pg.replace('src="script.js"', 'src="../assets/js/script.js"')
        pg = pg.replace('src="IMG-20260228-WA0205.jpg"', 'src="../assets/images/IMG-20260228-WA0205.jpg"')
        pg = pg.replace('href="index.html"', 'href="../index.html"')
        with open(path, 'w', encoding='utf-8') as f: f.write(pg)

for e in ['data.json', 'Profile.pdf', 'website_updates.log']:
    if os.path.exists(e): shutil.move(e, f'engine/{e}')

if os.path.exists('update_portfolio.py'):
    with open('update_portfolio.py', 'r', encoding='utf-8') as f: py = f.read()
    py = py.replace("'index.html'", "'../index.html'")
    for h in html_files: py = py.replace(f"'{h}'", f"'../pages/{h}'")
    # Fix Git staging
    py = py.replace("subprocess.run([git_path, 'add', '.'], check=True)", "subprocess.run([git_path, 'add', '.', '--all'], cwd='..', check=True)")
    py = py.replace("subprocess.run([git_path, 'commit', '-m', commit_msg], capture_output=True, text=True)", "subprocess.run([git_path, 'commit', '-m', commit_msg], cwd='..', capture_output=True, text=True)")
    py = py.replace("subprocess.run([git_path, 'push', '-u', 'origin', 'main'], check=True)", "subprocess.run([git_path, 'push', '-u', 'origin', 'main'], cwd='..', check=True)")
    with open('update_portfolio.py', 'w', encoding='utf-8') as f: f.write(py)
    shutil.move('update_portfolio.py', 'engine/update_portfolio.py')

if os.path.exists('USER_MANUAL.md'):
    with open('USER_MANUAL.md', 'r', encoding='utf-8') as f: man = f.read()
    man = man.replace(r'(`g:\My Drive\MYSITE\`)', r'(`g:\My Drive\MYSITE\engine\`)')
    man = man.replace('cd "G:\\My Drive\\MYSITE"', 'cd "G:\\My Drive\\MYSITE\\engine"')
    man = man.replace('python update_portfolio.py', 'python update_portfolio.py\n   (Note: Always run this explicitly from inside the `engine` folder!)')
    with open('USER_MANUAL.md', 'w', encoding='utf-8') as f: f.write(man)

print("Massive Architectural Refactor Complete!")
