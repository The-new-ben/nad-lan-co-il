# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

for name in ['ashira', 'rainbow']:
    with open(f'plugins/nadlan-config/assets/project-stage/{name}/stage.js', encoding='utf-8') as f:
        text = f.read()
    print(f'=== {name} ===')
    for m in re.finditer(r'addEventListener\([\'"](pointerdown|pointerup|click|mousedown)[\'"]', text):
        idx = m.start()
        print(text[idx:idx+120].replace('\n', ' '))
