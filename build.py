# src.html is the DB page body (also used for the claude.ai preview); db/index.html is the full document for GitHub Pages.
# The landing pages (index.html, ko/index.html) are built separately by build_landing.py.
import json, os, time
D = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(D, 'src.html'), encoding='utf-8').read()
i = src.index('</style>') + len('</style>')
head, body = src[:i], src[i:]
# the page now lives one folder down, so its local data fallback is ../data/
body = body.replace("pickup-island-league/data/data/', 'data/']", "pickup-island-league/data/data/', '../data/']")
html = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<link rel="icon" type="image/png" href="../assets/favicon-64.png">\n'
        '<meta property="og:title" content="Pickup Island League DB">\n'
        '<meta property="og:description" content="Standings, team pages, every player\'s ratings, leaders and league history — updated live from the 24/7 broadcast.">\n'
        '<meta property="og:image" content="https://bearhumans.github.io/pickup-island-league/assets/share.jpg">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
os.makedirs(os.path.join(D, 'db'), exist_ok=True)
open(os.path.join(D, 'db', 'index.html'), 'w', encoding='utf-8').write(html)
idx = []
for f in sorted(os.listdir(os.path.join(D, 'data'))):
    if f.startswith('league-') and f.endswith('.json'):
        s = json.load(open(os.path.join(D, 'data', f), encoding='utf-8'))
        idx.append({'loc': s.get('loc'), 'ch': s.get('ch'), 'at': s.get('at'), 'season': s.get('season'), 'round': s.get('round'), 'phase': s.get('phase')})
json.dump({'leagues': idx}, open(os.path.join(D, 'data', 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('built db/index.html', len(html), idx)
