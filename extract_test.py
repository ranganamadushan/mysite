import pypdf

reader = pypdf.PdfReader('Profile.pdf')
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

with open('profile.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("PDF Extracted!")
