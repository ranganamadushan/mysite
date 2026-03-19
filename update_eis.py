import json

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for app in d.get('applications', []):
    if 'EIS' in app.get('title', ''):
        app['url'] = 'https://ranganamadushan.github.io/EIS-/'
        if 'download' in app:
            app['download'] = False
        app['website'] = True

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=4)

print("Updated EIS app in data.json!")
