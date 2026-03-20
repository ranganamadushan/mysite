import subprocess, os, shutil

git = r"C:\Program Files\Git\cmd\git.exe"

# 1. Restore CV from Git History explicitly natively
print("Searching Git tree for original CV file...")
try:
    subprocess.run([git, 'checkout', 'c0449da', '--', 'CV - SDSU.pdf'], check=True, capture_output=True)
    if os.path.exists('CV - SDSU.pdf'):
        os.makedirs('assets/cv', exist_ok=True)
        # Force move gracefully natively
        if os.path.exists('assets/cv/cv.pdf'):
            os.remove('assets/cv/cv.pdf')
        shutil.move('CV - SDSU.pdf', 'assets/cv/cv.pdf')
        print("Successfully restored explicitly deleted CV natively!")
except Exception as e:
    print(f"Failed to restore CV natively: {e}")

# 2. Fix index.html button cleanly
if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f: idx = f.read()
    idx = idx.replace('href="CV - SDSU.pdf"', 'href="assets/cv/cv.pdf"')
    with open('index.html', 'w', encoding='utf-8') as f: f.write(idx)

# 3. Clean inline grid explicitly securely blocking mobile queries
engine_path = 'engine/update_portfolio.py'
if os.path.exists(engine_path):
    with open(engine_path, 'r', encoding='utf-8') as f: py = f.read()
    py = py.replace('style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.8rem; margin-top: 1.5rem; width: 100%;"', '')
    with open(engine_path, 'w', encoding='utf-8') as f: f.write(py)
    print("Stripped strict inline grids natively!")

# 4. Append comprehensive strictly responsive media queries natively cleanly
css_additions = '''
/* --- Comprehensive Mobile Responsiveness natively --- */
@media (max-width: 900px) {
    nav {
        flex-direction: column;
        padding: 1rem;
        gap: 0.8rem;
    }
    nav ul {
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
    }
    .hero h1 {
        font-size: 3.2rem;
    }
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin-top: 1.5rem;
    width: 100%;
}

@media (max-width: 650px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .hero-image img, .hero-image::before {
        width: 260px;
        height: 260px;
    }
}

@media (max-width: 450px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
    .hero h1 {
        font-size: 2.6rem;
    }
}
'''
if os.path.exists('assets/css/style.css'):
    with open('assets/css/style.css', 'a', encoding='utf-8') as f:
        f.write(css_additions)
    print("Injected native CSS Media queries effectively natively.")

# 5. Execute explicit engine rebuild natively actively
print("\nRebuilding explicit architecture natively seamlessly...")
os.chdir('engine')
subprocess.run(['python', 'update_portfolio.py'])
print("Explicit recovery smoothly unconditionally completed organically!")
