
import io
import sys
from pathlib import Path

p = Path('core/templates/index.html')
text = p.read_text(encoding='utf-8')
lines = text.splitlines()

out_lines = []
i = 0
n = len(lines)
while i < n:
    line = lines[i]
    if line.strip() == '<<<<<<< HEAD':
        i += 1
        while i < n and lines[i].strip() != '=======':
            i += 1
        # skip =======
        i += 1
        # collect lines until >>>>>>> sebas
        while i < n and not lines[i].strip().startswith('>>>>>>>'):
            out_lines.append(lines[i])
            i += 1
        # skip >>>>>>> ...
        if i < n and lines[i].strip().startswith('>>>>>>>'):
            i += 1
        continue
    else:
        out_lines.append(line)
        i += 1

p.write_text('\n'.join(out_lines), encoding='utf-8')
print('Done')
