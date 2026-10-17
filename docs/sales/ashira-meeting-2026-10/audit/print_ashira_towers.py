# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('plugins/nadlan-config/assets/project-stage/ashira/stage.js', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const\s+TOWERS\s*=\s*\[(.*?)\n\];', text, re.DOTALL)
if m:
    for block in re.findall(r'\{[^{}]*id:[^{}]*\}', m.group(1), re.DOTALL):
        print(block.strip())
        print('-'*40)
