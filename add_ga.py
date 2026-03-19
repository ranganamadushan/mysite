import os

ga_script = '''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZGXTSCN24V"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-ZGXTSCN24V');
    </script>
</head>'''

files = ['index.html', 'education.html', 'experience.html', 'projects.html', 'applications.html', 'publications.html']

for f in files:
    if not os.path.exists(f):
        print(f"Skipping {f}, doesn't exist.")
        continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if "G-ZGXTSCN24V" not in content:
        new_content = content.replace("</head>", ga_script)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
            
print("Added Google Analytics securely to all 6 HTML pages!")
