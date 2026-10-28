# Builds the public landing pages from the design exports in landing/.
#   landing/en.dc.html -> index.html      (English, site root)
#   landing/ko.dc.html -> ko/index.html   (Korean)
# Re-export the design, drop the two files into landing/, then run: python3 build_landing.py
import os, re

D = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://bearhumans.github.io/pickup-island-league/'
LIVE = 'https://www.youtube.com/@PickupIsland247/live'

# design asset ids -> files in assets/
BLOBS = {
    '33361741f9ed711215e2c1f6eead2045': 'live-court.jpg',
    '7bc8f6433a81de4fc46539f68c66b866': 'dunk-replay.jpg',
    '413c8a50d3a6785bd4df86b7eb95c47e': 'draft-night.png',
    '9ea625dea9cd5a09274163adb68d17c4': 'trade-desk.png',
    '263e2df5afd98f7a610862e35cfe6aa2': 'fa-live.png',
    'a94f47e5982058228e1cc24dff5f1e3f': 'player-card-ko.png',
    'f974c4448b80179a6aa88cb456c8181a': 'player-card-en.png',
    'b41fe43fee1c7bf881b3d11d107212b5': 'fan-ranking.png',
}

PAGES = {
    'en': dict(src='landing/en.dc.html', out='index.html', root='', other='ko/', other_src='Main.dc.html',
               db='League DB', url=SITE, locale='en_US',
               title='Pickup Island League — the basketball league that never sleeps',
               desc='A pixel-art basketball league run by AI and streamed live 24/7 on YouTube. 30 teams, 82-game seasons, trades, drafts and playoffs, with live commentary.'),
    'ko': dict(src='landing/ko.dc.html', out='ko/index.html', root='../', other='../', other_src='En.dc.html',
               db='리그 DB', url=SITE + 'ko/', locale='ko_KR',
               title='Pickup Island League — 꺼지지 않는 픽셀 농구 리그',
               desc='AI가 운영하는 픽셀 농구 리그가 유튜브에서 24시간 생중계돼요. 30개 구단, 82경기 시즌, 트레이드·드래프트·플레이오프와 실시간 중계.'),
}

# old links to the DB used the site root (/#team-ABC, /#player-12 ...); send them to db/
DB_ROUTE_REDIRECT = """<script>
(function(){var h=location.hash.slice(1),k=h.split('-')[0];
if(['home','standings','teams','team','players','player','leaders','history'].indexOf(k)>-1){location.replace('%sdb/#'+h);}})();
</script>"""

NAV_LINK = '<a href="{href}" style="color: #a3adc6; text-decoration: none">{label}</a>'


def build(lang, p):
    src = open(os.path.join(D, p['src']), encoding='utf-8').read()
    helmet = re.search(r'<helmet>(.*?)</helmet>', src, re.S).group(1).strip()
    body = re.search(r'</helmet>(.*?)</x-dc>', src, re.S).group(1).strip()
    for bid, name in BLOBS.items():
        body = body.replace('/_blob/' + bid, p['root'] + 'assets/' + name)
    if '/_blob/' in body:
        raise SystemExit(f'{lang}: unknown design image left in page — add it to BLOBS')
    body = body.replace(f'href="{p["other_src"]}"', f'href="{p["other"]}"')
    # DB link in the top menu (after patch notes) and in the footer
    body = re.sub(r'(<a href="#patch"[^>]*>[^<]*</a>)',
                  lambda m: m.group(1) + '\n' + NAV_LINK.format(href=p['root'] + 'db/', label=p['db']), body, count=1)
    body = body.replace('<a href="https://www.youtube.com/@PickupIsland247">YouTube @PickupIsland247</a>',
                        f'<span style="display: flex; flex-wrap: wrap; gap: 6px 18px"><a href="{p["root"]}db/">{p["db"]}</a>'
                        '<a href="https://www.youtube.com/@PickupIsland247">YouTube @PickupIsland247</a></span>', 1)
    img = SITE + 'assets/share.jpg'
    head = f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}">
<link rel="canonical" href="{p["url"]}">
<link rel="alternate" hreflang="en" href="{SITE}">
<link rel="alternate" hreflang="ko" href="{SITE}ko/">
<link rel="alternate" hreflang="x-default" href="{SITE}">
<meta name="theme-color" content="#0b1020">
<link rel="icon" type="image/png" href="{p["root"]}assets/favicon-64.png">
<link rel="apple-touch-icon" href="{p["root"]}assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pickup Island League">
<meta property="og:title" content="{p["title"]}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:url" content="{p["url"]}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{p["locale"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@PickupIsland247">
<meta name="twitter:title" content="{p["title"]}">
<meta name="twitter:description" content="{p["desc"]}">
<meta name="twitter:image" content="{img}">
{DB_ROUTE_REDIRECT % p["root"] if lang == "en" else ""}
{helmet}
<style>img{{max-width:100%}} html{{scroll-behavior:smooth}} @media (prefers-reduced-motion: reduce){{html{{scroll-behavior:auto}}}}</style>'''
    html = f'<!doctype html>\n<html lang="{lang}">\n<head>\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'
    out = os.path.join(D, p['out'])
    os.makedirs(os.path.dirname(out) or D, exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    print('built', p['out'], len(html))


for lang, p in PAGES.items():
    build(lang, p)
