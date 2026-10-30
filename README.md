# Pickup Island League

Public site for the 24/7 YouTube broadcast [@PickupIsland247](https://www.youtube.com/@PickupIsland247/live).

- Landing page: `index.html` (English) and `ko/index.html` (Korean), built from the design exports in `landing/` with `python3 build_landing.py`
- Patch notes, all versions: `patch-notes/index.html`, built from the landing exports by `python3 build_patch.py` (run after build_landing.py)
- Viewer guide: `guide/index.html` — how fans join a team, predict, draft a rookie and vote tactics from chat (Korean/English in one page)
- League DB: `db/index.html` — standings, team pages, every player's ratings, leaders and league history. Built from `src.html` with `python3 build.py`
- `db/ko.json`: the game's dictionary read backwards (English → Korean), so the Korean view of an English snapshot shows Korean ratings, styles and news. Regenerate from the game's i18n files when new strings are added.
- Data: `data/league-<lang>.json`, pushed by the broadcast machine after every round, plus `data/index.json`
- Old DB links on the site root (`/#team-…`, `/#player-…`, `/#standings` …) are forwarded to `db/`

## Play in the browser (`play/`)
- `play/index.html` — English game (copy of the "Pickup Island League · Global" artifact)
- `play/ko/index.html` — Korean game (copy of the "Pickup Island League" artifact)
These are snapshots. After publishing a new game version, copy the new HTML over these files and push.
The landing's "Be the GM in your browser" button points here (set in build_landing.py).
