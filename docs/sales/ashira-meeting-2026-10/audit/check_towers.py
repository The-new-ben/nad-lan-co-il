# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

for name in ['ashira', 'rainbow']:
    with open(f'plugins/nadlan-config/assets/project-stage/{name}/stage.js', encoding='utf-8') as f:
        text = f.read()
    print(f'=== {name} TOWERS ===')
    m = re.search(r'const\s+TOWERS\s*=\s*(\[.*?\]);', text, re.DOTALL)
    if m:
        print(m.group(1)[:500])
