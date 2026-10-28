# site/src.html is the page body (also used for the claude.ai preview); index.html is the full document for GitHub Pages
import json, os, time
D = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(D, 'src.html'), encoding='utf-8').read()
i = src.index('</style>') + len('</style>')
head, body = src[:i], src[i:]
html = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
open(os.path.join(D, 'index.html'), 'w', encoding='utf-8').write(html)
idx = []
for f in sorted(os.listdir(os.path.join(D, 'data'))):
    if f.startswith('league-') and f.endswith('.json'):
        s = json.load(open(os.path.join(D, 'data', f), encoding='utf-8'))
        idx.append({'loc': s.get('loc'), 'ch': s.get('ch'), 'at': s.get('at'), 'season': s.get('season'), 'round': s.get('round'), 'phase': s.get('phase')})
json.dump({'leagues': idx}, open(os.path.join(D, 'data', 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('built', len(html), idx)
