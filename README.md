# vibes

A personal image moodboard — scattered images, organized by year.

Inspired by [Guzey](https://guzey.com/vibes/) and [Sophia](https://girl.surgery/website_vibes/). Based on the approach from [sophiawisdom's gist](https://gist.github.com/sophiawisdom/c1b16fcaca017d1aec2358c6fb619697).

## setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install pillow pillow-heif
```

## structure

```
vibes/
├── 2026/       ← current year images go here
├── 2025/       ← older year
├── lister.py
└── venv/
```

A new year folder (e.g. `2027/`) is automatically picked up as the new current year next time you run `lister.py`. No manual changes needed.

## add images & generate

```bash
source venv/bin/activate
python3 lister.py
deactivate
```

## preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## deploy to github pages

```bash
git init
echo "venv/" >> .gitignore
git add .
git commit -m "init"
git remote add origin https://github.com/YOUR_USERNAME/vibes.git
git push -u origin main
```

Then go to repo → **Settings → Pages** → Source: `main` / `root` → Save.

Live at `https://YOUR_USERNAME.github.io/vibes/` in a minute.

To update after adding new images:

```bash
source venv/bin/activate && python3 lister.py && deactivate
git add . && git commit -m "add images" && git push
```

## license

MIT
