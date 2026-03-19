import json
with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
d['site_visits'] = 120
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=4)
print("Added site_visits to data.json!")
