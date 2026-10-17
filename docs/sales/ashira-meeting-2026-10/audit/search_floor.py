# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('plugins/nadlan-config/assets/project-stage/ashira/stage.js', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'(function\s+[a-zA-Z0-9_]*floor[a-zA-Z0-9_]*|const\s+[a-zA-Z0-9_]*floor[a-zA-Z0-9_]*\s*=|selectFloor|pickFloor|raycast)', text, re.IGNORECASE):
    idx = m.start()
    print(text[idx:idx+150].replace('\n', ' '))
