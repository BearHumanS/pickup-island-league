# Builds the full patch-notes page from the landing design exports.
#   landing/ko.dc.html + landing/en.dc.html -> patch-notes/index.html  (Korean/English in one page)
# The landing keeps the same notes inline; this page is the complete, linkable list. Run after build_landing.py.
import os, re, html

D = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://bearhumans.github.io/pickup-island-league/'
LIVE = 'https://www.youtube.com/@PickupIsland247/live'

def articles(path):
    s = open(os.path.join(D, path), encoding='utf-8').read()
    seg = s[s.index('id="patch"'):]
    out = []
    for a in re.findall(r'<article[\s\S]*?</article>', seg):
        ver = re.search(r'<h3[^>]*>(v\d+)</h3>', a).group(1)
        sub = re.search(r'<span style="color: #a3adc6[^"]*">([^<]*)</span>', a)   # the subtitle, not the LATEST badge
        items = [re.sub(r'<b style="[^"]*">', '<b>', li) for li in re.findall(r'<li>([\s\S]*?)</li>', a)]
        out.append({'v': ver, 'n': int(ver[1:]), 'sub': sub.group(1).strip() if sub else '', 'items': items})
    out.sort(key=lambda x: -x['n'])
    return out

# notes written before the landing existed (the landing's list starts at v82)
EARLY = {
    'ko': [('v75', '2026.10.26 · 경기 후 광고 시간', ['<b>경기 후 1분 광고</b>: 경기가 끝나면 최종 점수를 14초 보여 준 뒤 약 1분의 영상 광고 시간이 들어가요. 광고는 월 단위 선불 상품으로 팔아요.']),
           ('v74', '2026.10.26 · 구단 이름 스폰서', ['<b>팀 네이밍 스폰서</b>: 스폰서 이름이 구단 이름 앞에 붙어 점수판·해설·기록에 나와요. 방송 설정의 스폰서 탭에서 관리해요.'])],
    'en': [('v75', 'Oct 26, 2026 · Post-game ad break', ['<b>One-minute ad break after every game</b>: the final score holds for 14 s, then a video ad break of about a minute runs. Sold as prepaid monthly plans.']),
           ('v74', 'Oct 26, 2026 · Team naming sponsor', ['<b>Team naming sponsorship</b>: the sponsor name sits in front of the club name on the scorebug, in commentary and in the records. Managed from the Sponsors tab of the broadcast settings.'])],
}

T = {
    'ko': dict(title='Pickup Island 패치노트 — 전체', h1='패치노트 <em>전체</em>', lead='게임과 방송에 들어간 변경을 버전마다 적어 둔 기록이에요. 맨 위가 최신이고, 버전 번호를 누르면 그 항목으로 내려가요. 현재 방송은 {cur} 기준이에요.',
               count='{n}개 버전 · {a}~{b}', early='v82 이전 기록은 랜딩 페이지를 만들기 전이라 요약만 남아 있어요.', db='리그 DB', guide='참여 안내', ad='광고 문의', live='라이브 보기', home='홈', latest='최신', jump='버전으로 이동',
               foot='변경 이력은 랜딩 페이지의 패치노트와 같은 내용이에요.'),
    'en': dict(title='Pickup Island patch notes — all versions', h1='All <em>patch notes</em>', lead='Every change to the game and the broadcast, version by version. Newest first; tap a version number to jump to it. The broadcast currently runs {cur}.',
               count='{n} versions · {a}–{b}', early='Notes before v82 predate the landing page, so only a summary survives.', db='League DB', guide='Viewer guide', ad='Advertise', live='Watch live', home='Home', latest='LATEST', jump='Jump to a version',
               foot='Same notes as the patch section of the landing page.'),
}

def render(lang, arts):
    t = T[lang]
    cur = arts[0]['v']
    all_arts = arts + [{'v': v, 'n': int(v[1:]), 'sub': sub, 'items': items, 'early': True} for v, sub, items in EARLY[lang]]
    jumps = ''.join(f'<a href="#{lang}-{a["v"]}">{a["v"]}</a>' for a in all_arts)
    body = []
    for i, a in enumerate(all_arts):
        if a.get('early') and (i == 0 or not all_arts[i - 1].get('early')):
            body.append(f'<p class="early">{t["early"]}</p>')
        lis = ''.join(f'<li>{li}</li>' for li in a['items'])
        body.append(f'<article id="{lang}-{a["v"]}" class="{"latest" if i == 0 else ""}"><header><h2>{a["v"]}</h2>{"<span class=badge>" + t["latest"] + "</span>" if i == 0 else ""}<span class="sub">{html.escape(a["sub"])}</span></header><ul>{lis}</ul></article>')
    return f'''<section class="hero"><div class="wrap">
  <p class="eyebrow">Patch notes</p>
  <h1>{t["h1"]}</h1>
  <p class="lead">{t["lead"].format(cur=cur)}</p>
  <p class="count">{t["count"].format(n=len(all_arts), a=all_arts[-1]["v"], b=cur)}</p>
</div></section>
<nav class="jump" aria-label="{t["jump"]}"><div class="wrap"><span class="jl">{t["jump"]}</span>{jumps}</div></nav>
<div class="wrap notes">{"".join(body)}</div>
<footer><div class="wrap">{t["foot"]} · <a href="{'../ko/' if lang == 'ko' else '../'}">{t["home"]}</a> · <a href="../db/">{t["db"]}</a> · <a href="../guide/#{lang}">{t["guide"]}</a> · <a href="../advertise/{'#ko' if lang == 'ko' else ''}">{t["ad"]}</a></div></footer>'''

ko, en = articles('landing/ko.dc.html'), articles('landing/en.dc.html')
page = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Pickup Island 패치노트 — 전체 · All patch notes</title>
<meta name="description" content="Pickup Island Basketball 24/7의 역대 패치노트 전체: 경기 엔진, 선수 AI, 코치, 방송 화면, 리그 DB의 버전별 변경. The complete changelog of the 24/7 pixel basketball league.">
<link rel="canonical" href="{SITE}patch-notes/">
<meta name="theme-color" content="#0d0f24">
<link rel="icon" type="image/png" href="../assets/favicon-64.png">
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pickup Island League">
<meta property="og:title" content="Pickup Island 패치노트 — 전체 · All patch notes">
<meta property="og:description" content="역대 패치노트 전체 · The complete changelog, newest first.">
<meta property="og:url" content="{SITE}patch-notes/">
<meta property="og:image" content="{SITE}assets/share.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@PickupIsland247">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Silkscreen:wght@400;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
/* Layout: the night-court look of the other pages. One 900px reading column; a sticky version strip under the bar; one card per version, newest first. */
:root {{ color-scheme: dark; --night: #0d0f24; --night-2: #161a3a; --line: #2b3062; --ink: #f3f1ea; --ink-soft: #b9bcdc; --faint: #7f84ad; --orange: #ff8a3d; --gold: #f2b630; --court: #46d0c4;
  --pixel: "Silkscreen", "Courier New", monospace; --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace; --body: "IBM Plex Sans", "Noto Sans KR", system-ui, sans-serif; --body-ko: "Noto Sans KR", "IBM Plex Sans", system-ui, sans-serif; }}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}
body {{ margin: 0; background: var(--night); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.6; }}
body.ko {{ font-family: var(--body-ko); word-break: keep-all; }}
[hidden] {{ display: none !important; }}
.wrap {{ max-width: 900px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
a {{ color: var(--orange); }}
a:focus-visible, button:focus-visible {{ outline: 2px solid var(--orange); outline-offset: 3px; }}
h1, h2 {{ margin: 0; line-height: 1.15; text-wrap: balance; }}
p {{ margin: 0; text-wrap: pretty; }}
.eyebrow {{ font-family: var(--pixel); font-size: 13px; letter-spacing: 0.12em; color: var(--orange); text-transform: uppercase; }}
body::before {{ content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--night); }}
.bar {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: rgba(13, 15, 36, 0.94); border-bottom: 1px solid var(--line); backdrop-filter: blur(6px); }}
.bar .wrap {{ display: flex; align-items: center; gap: 14px; padding-block: 10px; flex-wrap: wrap; }}
.brand {{ display: flex; align-items: center; gap: 10px; color: var(--ink); text-decoration: none; margin-right: auto; }}
.brand img {{ width: 40px; height: 40px; border-radius: 50%; }}
.brand span {{ font-family: var(--pixel); font-size: 15px; line-height: 1.1; }}
.navl {{ color: var(--ink-soft); text-decoration: none; font-weight: 600; font-size: 14px; }} .navl:hover {{ color: var(--ink); }}
.lang {{ display: inline-flex; border: 1px solid var(--line); }}
.lang button {{ font: 600 14px var(--body); color: var(--ink-soft); background: transparent; border: 0; padding: 8px 14px; min-height: 40px; cursor: pointer; }}
.lang button[aria-pressed="true"] {{ background: var(--ink); color: var(--night); }}
.btn {{ display: inline-flex; align-items: center; min-height: 44px; padding: 0 18px; font: 700 15px var(--body); background: var(--orange); color: var(--night); text-decoration: none; }}
.btn:hover {{ background: #ffa265; }}
.hero {{ border-bottom: 1px solid var(--line); background: radial-gradient(1000px 420px at 85% 0%, #1e2350 0%, var(--night) 70%); }}
.hero .wrap {{ padding-block: 48px 36px; display: flex; flex-direction: column; gap: 14px; }}
.hero h1 {{ font-size: clamp(30px, 5vw, 48px); font-weight: 700; letter-spacing: -0.01em; }}
.hero h1 em {{ font-style: normal; color: var(--orange); }}
.hero .lead {{ font-size: 17px; color: var(--ink-soft); max-width: 40em; }}
.hero .count {{ font: 600 13px var(--mono); letter-spacing: .06em; color: var(--court); }}
.jump {{ position: sticky; top: calc(env(safe-area-inset-top, 0px) + 65px); z-index: 4; background: rgba(13, 15, 36, 0.96); border-bottom: 1px solid var(--line); }}
.jump .wrap {{ display: flex; flex-wrap: wrap; gap: 6px; padding-block: 10px; align-items: center; }}
.jump .jl {{ font: 600 11px var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--faint); margin-right: 6px; }}
.jump a {{ font: 600 12px var(--mono); color: var(--ink-soft); text-decoration: none; border: 1px solid var(--line); padding: 3px 8px; }}
.jump a:hover {{ color: var(--ink); border-color: var(--ink-soft); }}
.notes {{ display: flex; flex-direction: column; gap: 18px; padding-block: 32px 48px; }}
article {{ background: var(--night-2); border: 1px solid var(--line); padding: 24px 26px; display: flex; flex-direction: column; gap: 12px; scroll-margin-top: 130px; }}
article.latest {{ border-color: var(--orange); }}
article header {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px 14px; }}
article h2 {{ font: 700 24px var(--pixel); color: var(--gold); letter-spacing: .02em; }}
article .badge {{ font: 700 10px var(--pixel); letter-spacing: .12em; background: var(--orange); color: var(--night); padding: 3px 8px; }}
article .sub {{ color: var(--ink-soft); font-size: 15px; }}
article ul {{ margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px; color: #c6cde0; }}
article li b {{ color: var(--ink); }}
.early {{ color: var(--faint); font-size: 14px; padding: 8px 0 0; border-top: 1px dashed var(--line); }}
footer {{ border-top: 1px solid var(--line); padding-block: 24px 40px; color: var(--faint); font-size: 13px; }}
footer a {{ color: var(--ink-soft); }}
@media (max-width: 640px) {{ .jump {{ position: static; }} article {{ padding: 18px 16px; scroll-margin-top: 80px; }} }}
</style>
</head>
<body class="ko">
<header class="bar"><div class="wrap">
  <a class="brand" href="../ko/"><img src="../assets/logo-512.png" alt=""><span>PICKUP ISLAND<br>BASKETBALL 24/7</span></a>
  <a class="navl" href="../db/" data-en="League DB" data-ko="리그 DB">리그 DB</a>
  <a class="navl" href="../guide/" data-en="Viewer guide" data-ko="참여 안내">참여 안내</a>
  <div class="lang" role="group" aria-label="Language"><button type="button" data-lang="ko" aria-pressed="true">한국어</button><button type="button" data-lang="en" aria-pressed="false">EN</button></div>
  <a class="btn" href="{LIVE}" target="_blank" rel="noopener" data-en="Watch live" data-ko="라이브 보기">라이브 보기</a>
</div></header>
<div id="ko">{render('ko', ko)}</div>
<div id="en" hidden>{render('en', en)}</div>
<script>
(function () {{
  var panes = {{ en: document.getElementById('en'), ko: document.getElementById('ko') }};
  var btns = document.querySelectorAll('.lang button');
  function setLang(l) {{
    if (!panes[l]) l = 'ko';
    panes.en.hidden = l !== 'en'; panes.ko.hidden = l !== 'ko';
    document.documentElement.lang = l; document.body.classList.toggle('ko', l === 'ko');
    btns.forEach(function (b) {{ b.setAttribute('aria-pressed', String(b.dataset.lang === l)); }});
    document.querySelectorAll('[data-en]').forEach(function (el) {{ el.textContent = el.dataset[l] || el.dataset.en; }});
    document.querySelectorAll('.navl[href^="../guide/"]').forEach(function (a) {{ a.href = '../guide/#' + l; }});
    try {{ localStorage.setItem('pil-guide-lang', l); }} catch (e) {{}}
  }}
  var start = 'ko', h = location.hash;
  try {{ var s = localStorage.getItem('pil-guide-lang'); if (s === 'en' || s === 'ko') start = s; else if (!/^ko/i.test(navigator.language || '')) start = 'en'; }} catch (e) {{}}
  if (h === '#en' || /^#en-/.test(h)) start = 'en';
  if (h === '#ko' || /^#ko-/.test(h)) start = 'ko';
  if (/^#v\\d+$/.test(h)) {{ h = '#' + start + '-' + h.slice(1); }}   // #v104 works in either language
  setLang(start);
  if (/^#(ko|en)$/.test(h)) {{ var up = function () {{ window.scrollTo(0, 0); }}; up(); setTimeout(up, 0); setTimeout(up, 120); window.addEventListener('load', up); }}
  else if (/^#(ko|en)-v\\d+$/.test(h)) {{ var el = document.querySelector(h); if (el) setTimeout(function () {{ el.scrollIntoView(); }}, 60); }}
  btns.forEach(function (b) {{ b.addEventListener('click', function () {{ setLang(b.dataset.lang); if (/^#(ko|en)(-v\\d+)?$/.test(location.hash)) history.replaceState(null, '', location.hash.replace(/^#(ko|en)/, '#' + b.dataset.lang)); }}); }});
}})();
</script>
</body>
</html>
'''
os.makedirs(os.path.join(D, 'patch-notes'), exist_ok=True)
open(os.path.join(D, 'patch-notes', 'index.html'), 'w', encoding='utf-8').write(page)
print('built patch-notes/index.html', len(page), 'ko', len(ko), 'en', len(en), ko[0]['v'])
