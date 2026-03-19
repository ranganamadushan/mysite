import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data['research_interests'] = [
    'Condensed Matter Physics', 
    'Printed Flexible/Wearable Electronics', 
    'Material Physics', 
    'Wireless Communication', 
    'Sensor Fabrication'
]

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Added research interests to data.json!")
