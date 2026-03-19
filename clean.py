content = open('experience.html', 'r', encoding='utf-8').read()
idx1 = content.find('<h2 class="section-title">Selected Projects</h2>')
if idx1 != -1:
    idx2 = content.find('</section>', idx1)
    new_content = content[:idx1] + content[idx2:]
    open('experience.html', 'w', encoding='utf-8').write(new_content)
    print("Stripped Projects from experience.html")
else:
    print("Already stripped.")
