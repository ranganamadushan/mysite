import json
import os
import re
import requests
import sys
import logging
from bs4 import BeautifulSoup

# Configure persistent logging for website updates
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('website_updates.log', encoding='utf-8')
fh.setFormatter(formatter)
logger.addHandler(fh)

def log_print(*args, **kwargs):
    logger.info(" ".join(map(str, args)))
    
# Override built-in print to capture all engine events globally
import builtins
builtins.print = log_print

def replace_in_file(filename, start_marker, end_marker, new_content):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = f"({start_marker}).*?({end_marker})"
    replacement = f"\\1\n{new_content}\n                \\2"
    
    new_doc, num_subs = re.subn(pattern, replacement, content, flags=re.DOTALL)
    
    if num_subs > 0:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_doc)
        print(f"Updated {filename} successfully.")
    else:
        print(f"Could not find markers in {filename}.")


def parse_linkedin_pdf(pdf_path):
    try:
        import pypdf
    except ImportError:
        print("pypdf is required. Run: python -m pip install pypdf")
        return None, None
        
    try:
        reader = pypdf.PdfReader(pdf_path)
    except FileNotFoundError:
        print(f"Could not find {pdf_path}. Make sure it is in the same folder.")
        return None, None
        
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
        
    # Clean pagination markers
    text = re.sub(r'\s*Page \d+ of \d+\s*', '\n', text)
    
    exp_idx = text.find('\nExperience\n')
    edu_idx = text.find('\nEducation\n')
    
    if exp_idx == -1 or edu_idx == -1:
        print("Could not find the standard 'Experience' or 'Education' headers in the PDF.")
        return None, None
        
    exp_text = text[exp_idx+12:edu_idx].strip()
    edu_text = text[edu_idx+11:].strip()
    
    # Parse Education
    education = []
    edu_lines = [line.strip() for line in edu_text.split('\n') if line.strip()]
    i = 0
    while i < len(edu_lines) - 1:
        inst = edu_lines[i]
        details = edu_lines[i+1]
        if '·' in details:
            parts = details.split('·')
            degree = parts[0].strip()
            date = parts[1].strip().strip('()').strip()
            education.append({
                "degree": degree,
                "institution": f"{inst} | {date}",
                "description": ""
            })
            i += 2
        else:
            i += 1

    # Parse Experience
    experiences = []
    exp_lines = [line.strip() for line in exp_text.split('\n') if line.strip()]
    
    current_company = ""
    i = 0
    while i < len(exp_lines):
        line = exp_lines[i]
        
        # Rollup company duration
        if re.search(r'\d+\s+years?\s+\d+\s+months?', line) and '-' not in line:
            current_company = exp_lines[i-1]
            i += 1
            continue
            
        # Match time duration ex: "January 2026 - Present"
        months_pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December)'
        if re.search(months_pattern + r'\s+\d{4}\s*-\s*', line):
            role = exp_lines[i-1] if i > 0 else ""
            company = current_company
            if not company and i >= 2:
                company = exp_lines[i-2]
                
            period = line.split('(')[0].strip()
            experiences.append({
                "role": role,
                "company": f"{company} | {period}",
                "description": ""
            })
            current_company = ""
        i += 1
            
    return education, experiences


def update_from_pdf():
    print("--- Parsing LinkedIn Profile.pdf ---")
    education, experiences = parse_linkedin_pdf("Profile.pdf")
    
    if education is not None and experiences is not None:
        print(f"Extracted {len(education)} education items and {len(experiences)} experience items.")
        
        # Update data.json
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {}
            
        data['education'] = education
        data['experience'] = experiences
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
        print("Updated data.json successfully with new PDF data!")
    else:
        print("Parsing Failed. Will just rebuild from existing data.json.")


def rebuild_html_from_local():
    print("Loading Experience & Education from data.json...")
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("data.json not found! Please ensure it exists.")
        return

    # Generate Education
    edu_html = ""
    for ed in data.get('education', []):
        edu_html += f'''                <div class="timeline-item">
                    <div class="timeline-content">
                        <h3>{ed.get('degree','')}</h3>
                        <h4>{ed.get('institution','')}</h4>
                        <p>{ed.get('description','')}</p>
                    </div>
                </div>\n'''
    replace_in_file('education.html', '<!-- EDUCATION_START -->', '<!-- EDUCATION_END -->', edu_html)

    # Generate Experience
    exp_html = ""
    for exp in data.get('experience', []):
        exp_html += f'''                <div class="timeline-item">
                    <div class="timeline-content">
                        <h3>{exp.get('role','')}</h3>
                        <h4>{exp.get('company','')}</h4>
                        <p>{exp.get('description','')}</p>
                    </div>
                </div>\n'''
    replace_in_file('experience.html', '<!-- EXPERIENCE_START -->', '<!-- EXPERIENCE_END -->', exp_html)
    
    # Generate Projects
    proj_html = ""
    for proj in data.get('projects', []):
        tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in proj.get('tags', [])])
        
        button_html = ""
        if proj.get('download'):
            button_html = '<div style="margin-top: 1rem; margin-bottom: 0.5rem;"><span class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;"><i class="fas fa-download"></i> Download .exe</span></div>'
            
        proj_html += f'''                <a href="{proj.get('url','#')}" target="_blank" class="card">
                    <h3>{proj.get('title','')}</h3>
                    <span class="meta">{proj.get('period','')}</span>
                    <p>{proj.get('description','')}</p>
                    {button_html}
                    <div class="tag-list">
                        {tags_html}
                    </div>
                </a>\n'''
    replace_in_file('projects.html', '<!-- PROJECTS_START -->', '<!-- PROJECTS_END -->', proj_html)

    # Generate Applications
    app_html = ""
    for app in data.get('applications', []):
        tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in app.get('tags', [])])
        
        button_html = ""
        if app.get('download'):
            button_html = '<div style="margin-top: 1rem; margin-bottom: 0.5rem;"><span class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.85rem; background: rgba(255, 255, 255, 0.1);"><i class="fas fa-download"></i> View / Download App</span></div>'
        elif app.get('website'):
            button_html = '<div style="margin-top: 1rem; margin-bottom: 0.5rem;"><span class="btn btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;"><i class="fas fa-external-link-alt"></i> Open Web App</span></div>'
            
        app_html += f'''                <a href="{app.get('url','#')}" target="_blank" class="card">
                    <h3>{app.get('title','')}</h3>
                    <span class="meta">{app.get('period','')}</span>
                    <p>{app.get('description','')}</p>
                    {button_html}
                    <div class="tag-list">
                        {tags_html}
                    </div>
                </a>\n'''
    replace_in_file('applications.html', '<!-- APPLICATIONS_START -->', '<!-- APPLICATIONS_END -->', app_html)

    # Index Quick Info
    latest_job = data.get('experience', [{}])[0] if data.get('experience') else {}
    highest_edu = data.get('education', [{}])[0] if data.get('education') else {}
    interests = data.get('research_interests', [])
    interests_html = "".join([f'<span class="tag" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2);">{i}</span>' for i in interests])
    
    quick_info = f'''                <div class="info-card" style="background: rgba(255,255,255,0.03); padding: 1.5rem; border-radius: 12px; margin-top: 1.5rem; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.1); text-align: left;">
                    <h4 style="margin-bottom: 0.3rem; color: var(--accent); font-size: 1.05rem;"><i class="fas fa-briefcase"></i> Latest Role</h4>
                    <p style="margin-bottom: 1.2rem; margin-top: 0; font-size: 1rem;">{latest_job.get('role', '')} <br><span style="color: var(--text-secondary); font-size: 0.9rem;">{latest_job.get('company', '').split('|')[0].strip()}</span></p>
                    
                    <h4 style="margin-bottom: 0.3rem; color: var(--accent); font-size: 1.05rem;"><i class="fas fa-graduation-cap"></i> Highest Qualification</h4>
                    <p style="margin-bottom: 1.2rem; margin-top: 0; font-size: 1rem;">{highest_edu.get('degree', 'Unknown Degree').replace("Master's Degree,", "").strip()} <br><span style="color: var(--text-secondary); font-size: 0.9rem;">{highest_edu.get('institution', '').split('|')[0].strip()}</span></p>
                    
                    <h4 style="margin-bottom: 0.5rem; color: var(--accent); font-size: 1.05rem;"><i class="fas fa-microscope"></i> Research Interests</h4>
                    <div class="tag-list" style="margin-top: 0.5rem; justify-content: flex-start; gap: 0.5rem;">
                        {interests_html}
                    </div>
                </div>'''
    replace_in_file('index.html', '<!-- QUICK_INFO_START -->', '<!-- QUICK_INFO_END -->', quick_info)


def update_scholar(scholar_id):
    print(f"Fetching Google Scholar data for ID: {scholar_id}...")
    url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch Scholar profile")
            return
            
        soup = BeautifulSoup(response.text, 'html.parser')
        pubs_html = ""
        
        articles = soup.find_all('tr', class_='gsc_a_tr')
        if not articles:
            print("No articles found on Scholar page.")
            return

        for article in articles:
            title_elem = article.find('a', class_='gsc_a_at')
            title = title_elem.text if title_elem else "Unknown Title"
            
            meta = article.find_all('div', class_='gs_gray')
            authors = meta[0].text if len(meta) > 0 else ""
            venue = meta[1].text if len(meta) > 1 else ""
                
            pubs_html += f'''                <div class="pub-item">
                    <div class="pub-title">{title}</div>
                    <div class="pub-authors">{authors}</div>
                    <div class="pub-venue"><i class="fas fa-journal-whills"></i> {venue}</div>
                </div>\n'''
                
        replace_in_file('publications.html', '<!-- PUBLICATIONS_START -->', '<!-- PUBLICATIONS_END -->', pubs_html)
        print("Successfully updated publications from Google Scholar.")
        
        # Build Stats Grid
        stats_data = soup.find_all('td', class_='gsc_rsb_std')
        citations = stats_data[0].text if len(stats_data) >= 5 else "0"
        h_index = stats_data[2].text if len(stats_data) >= 5 else "0"
        i10_index = stats_data[4].text if len(stats_data) >= 5 else "0"
        pub_count = len(articles)
        
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {}
            
        proj_count = len(data.get('projects', []))
        visits = data.get('site_visits', 120)
        
        stats_html = f'''<!-- STATS_START -->
                <div class="stats-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.8rem; margin-top: 1.5rem; width: 100%;">
                    <div class="stat-box" style="background: rgba(255,255,255,0.03); padding: 0.8rem; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 1.3rem; font-weight: 800; color: var(--accent); margin-bottom: 0.2rem;">{pub_count}</div>
                        <div style="font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px;">Publications</div>
                    </div>
                    <div class="stat-box" style="background: rgba(255,255,255,0.03); padding: 0.8rem; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 1.3rem; font-weight: 800; color: var(--accent); margin-bottom: 0.2rem;">{h_index}</div>
                        <div style="font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px;">H-Index</div>
                    </div>
                    <div class="stat-box" style="background: rgba(255,255,255,0.03); padding: 0.8rem; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 1.3rem; font-weight: 800; color: var(--accent); margin-bottom: 0.2rem;">{i10_index}</div>
                        <div style="font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px;">i10-Index</div>
                    </div>
                    <div class="stat-box" style="background: rgba(255,255,255,0.03); padding: 0.8rem; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 1.3rem; font-weight: 800; color: var(--accent); margin-bottom: 0.2rem;">{citations}</div>
                        <div style="font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px;">Citations</div>
                    </div>
                    <div class="stat-box" style="background: rgba(255,255,255,0.03); padding: 0.8rem; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 1.3rem; font-weight: 800; color: var(--accent); margin-bottom: 0.2rem;">{proj_count}</div>
                        <div style="font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px;">Projects</div>
                    </div>
                    <div class="stat-box" style="background: rgba(255,255,255,0.03); padding: 0.8rem; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 1.3rem; font-weight: 800; color: var(--accent); margin-bottom: 0.2rem;">{visits}+</div>
                        <div style="font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px;">Site Visits</div>
                    </div>
                </div>
                <!-- STATS_END -->'''
        replace_in_file('index.html', '<!-- STATS_START -->', '<!-- STATS_END -->', stats_html)
        print("Successfully injected metrics grid into index.html")
        
    except Exception as e:
        print(f"Error fetching Scholar data: {e}")

if __name__ == "__main__":
    print("--- Starting Portfolio Automation ---")
    update_from_pdf()
    rebuild_html_from_local()
    # 3. Update Publications from Google Scholar
    scholar_id = "Um_jCEMAAAAJ" # Your Google Scholar ID
    update_scholar(scholar_id)
    
    print("--- Update Complete! ---")
    
    # 4. Auto-Commit and Push via explicitly targeted embedded Windows Git
    import subprocess
    from datetime import datetime
    import os
    
    def auto_commit_and_push():
        git_path = r"C:\Program Files\Git\cmd\git.exe"
        if not os.path.exists(git_path):
            print("Git not found explicit path. Please push manually.")
            return
            
        print("--- Starting Auto-Deploy to GitHub ---")
        try:
            subprocess.run([git_path, 'add', '.'], check=True)
            commit_msg = f"Automated Portfolio Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            result = subprocess.run([git_path, 'commit', '-m', commit_msg], capture_output=True, text=True)
            
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                print("No files were changed. Skipping deployment push.")
                return
                
            print("Pushing files securely to GitHub repository...")
            subprocess.run([git_path, 'push', '-u', 'origin', 'main'], check=True)
            print("Successfully explicitly deployed website to live server!")
        except Exception as e:
            print(f"Failed to auto-deploy to Github: {e}")
            
    auto_commit_and_push()
