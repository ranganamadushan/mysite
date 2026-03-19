import json
import os

# 1. Update data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'applications' not in data:
    data['applications'] = []

moodle_proj = None
for p in data.get('projects', []):
    if p.get('title') == 'Moodle Assignment Unzipper':
        moodle_proj = p
        break

if moodle_proj:
    data['projects'].remove(moodle_proj)
    if not any(a.get('title') == 'Moodle Assignment Unzipper' for a in data['applications']):
        data['applications'].append(moodle_proj)

eis_proj = {
    "title": "EIS Viewer App",
    "period": "Data Analysis Utility",
    "url": "https://github.com/ranganamadushan/EIS-",
    "description": "A comprehensive Python-based desktop application for visualizing, analyzing, and interactively processing Electrochemical Impedance Spectroscopy (EIS) experimental data.",
    "tags": ["Python", "Data Analysis", "Desktop App"],
    "download": True
}
if not any(a.get('title') == 'EIS Viewer App' for a in data['applications']):
    data['applications'].append(eis_proj)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

# 2. Add Navigation
files = ['index.html', 'education.html', 'experience.html', 'projects.html', 'publications.html']
for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if "applications.html" not in html:
        pub_link_idx = html.find('<li><a href="publications.html"')
        if pub_link_idx != -1:
            injection = '<li><a href="applications.html" class="nav-link">Applications</a></li>\n            '
            new_html = html[:pub_link_idx] + injection + html[pub_link_idx:]
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_html)

# 3. Create applications.html
with open('projects.html', 'r', encoding='utf-8') as f:
    proj_html = f.read()

app_html = proj_html.replace('Rangana Manamendra | Projects', 'Rangana Manamendra | Applications')
app_html = app_html.replace('href="projects.html" class="nav-link active"', 'href="projects.html" class="nav-link"')

if "applications.html" not in app_html:
    pub_link_idx = app_html.find('<li><a href="publications.html"')
    if pub_link_idx != -1:
        injection = '<li><a href="applications.html" class="nav-link active">Applications</a></li>\n            '
        app_html = app_html[:pub_link_idx] + injection + app_html[pub_link_idx:]
else:
    app_html = app_html.replace('href="applications.html" class="nav-link"', 'href="applications.html" class="nav-link active"')

app_html = app_html.replace('Selected Projects', 'Desktop Applications & Utilities')
app_html = app_html.replace('<!-- PROJECTS_START -->', '<!-- APPLICATIONS_START -->')
app_html = app_html.replace('<!-- PROJECTS_END -->', '<!-- APPLICATIONS_END -->')

with open('applications.html', 'w', encoding='utf-8') as f:
    f.write(app_html)

print("Generated applications.html and successfully updated JSON database + Global Nav links.")
