# vibes

A personal image moodboard. Inspired by [Xavi](https://hyuki.dev), [Guzey](https://guzey.com/vibes/), and [Sophia](https://girl.surgery/website_vibes/).

Original code by [sophiawisdom](https://gist.github.com/sophiawisdom/c1b16fcaca017d1aec2358c6fb619697).

---

## setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install pillow pillow-heif
```

## structure

```
vibes/
├── 2026/       ← drop images here (current year)
├── 2025/       ← older year
├── lister.py
└── venv/
```

## usage

Add images to the appropriate year folder, then run:

```bash
source venv/bin/activate
python3 lister.py
deactivate
```

This generates `index.html`, `images.json`, and `YEAR/index.html` for each older year.

A new year folder (e.g. `2027/`) is automatically picked up as the new current year next time you run `lister.py`.

## preview locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## deploy to github pages

1. Create a repo on GitHub (e.g. `vibes`)
2. Initialize and push:

```bash
git init
echo "venv/" >> .gitignore
git add .
git commit -m "init"
git remote add origin https://github.com/YOUR_USERNAME/vibes.git
git push -u origin main
```

3. Go to your repo on GitHub → **Settings** → **Pages**
4. Under *Source*, select **main** branch and **/ (root)**
5. Click **Save**

Your site will be live at `https://YOUR_USERNAME.github.io/vibes/` in a minute or two.

Every time you add images: run `lister.py`, commit, and push.

```bash
source venv/bin/activate && python3 lister.py && deactivate
git add .
git commit -m "add images"
git push
```
