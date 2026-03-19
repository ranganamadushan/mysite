import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_project = {
    "title": "Moodle Assignment Unzipper",
    "period": "Utility Tool",
    "url": "https://github.com/ranganamadushan/Unzip_for_moodle/raw/master/dist/unzip.exe",
    "description": "A lightweight customized executable built to automatically mass-unzip and organize student assignment submissions downloaded from Moodle LMS.",
    "tags": ["Python", "Automation", "Utility"],
    "download": True
}

if not any(p.get("title") == new_project["title"] for p in data["projects"]):
    data["projects"].insert(0, new_project)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print("Project added to data.json!")
else:
    print("Project already in data.json.")
