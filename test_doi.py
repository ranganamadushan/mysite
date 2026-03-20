import requests
import urllib.parse
titles = ["Direct writing of a graphene-based electrochemical impedance sensor on paper for wearable electronic applications",
          "An innovative approach to control and analyze Electro-Chemical Impedance Spectroscopy Data using Python"]

for title in titles:
    c_url = f"https://api.crossref.org/works?query.title={urllib.parse.quote(title)}&select=DOI,URL,title&rows=1"
    try:
        c_resp = requests.get(c_url, timeout=5, headers={'User-Agent': 'mailto:ranganamadushan@example.com'})
        items = c_resp.json().get('message', {}).get('items', [])
        if items:
            item = items[0]
            print(f"TITLE: {title}")
            print(f"FOUND: {item.get('title', ['None'])[0]}")
            print(f"DOI: {item.get('DOI')}\n")
        else:
            print(f"No items found for {title}\n")
    except Exception as e:
        print("Error:", e)
